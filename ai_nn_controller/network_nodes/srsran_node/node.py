# Copyright (c) 2026 Trinity College Dublin
#
# This file is dual-licensed:
# - under the AGPL (see LICENSE)
# - under a commercial licence (contact infoknex@tcd.ie)

"""srsRAN Network Node for ai_nn_controller.

Polls InfluxDB for the latest srsRAN metrics (same data source Grafana
uses) and forwards them as measurements through the ai_nn_controller message bus.

Recognises the SET_RRM_POLICY control command. Live configuration execution
is intentionally disabled until safety and recovery mechanisms are ready.
"""

from controlled_entity import ControlledEntity, node, NodeRunner
import threading
import time
from time import sleep
import json
from urllib.request import Request, urlopen
import os
import websocket


@node(name="srsRAN")
class SrsranNode(ControlledEntity):
    available_measurements = [
        "session_id",

        # OCUDU cell and DU metrics
        "cell_average_latency",
        "du_high_mac_dl_0_cpu_usage_percent",
        "du_high_mac_dl_0_average_latency_us",

        # UE-level metrics (from ue_info measurement)
        "pci",
        "rnti",
        "dl_bitrate",
        "ul_bitrate",
        "dl_bler",
        "ul_bler",
        "dl_mcs",
        "ul_mcs",
        "dl_nof_ok",
        "dl_nof_nok",
        "ul_nof_ok",
        "ul_nof_nok",
        "bsr",
        "cqi",
        "ri",
        "ul_snr",
        "pusch_snr_db",
        "pucch_snr_db",
        # System-level metrics (from app_resource_usage measurement)
        "cpu_usage_percent",
        "memory_usage_MB",
        "power_consumption_Watts",
    ]
    available_controls = ["SET_RRM_POLICY"]
    measurement_interval = 1.0

    def setup(self):
        """Start InfluxDB poller thread."""
        self._latest_metrics = {}
        self._metrics_lock = threading.Lock()

        self._influx_url = self.config.get("influxdb_url", "http://influxdb:8086")
        self._influx_token = os.environ.get("INFLUXDB_TOKEN") or self.config.get("influxdb_token", "")
        self._influx_org = self.config.get("influxdb_org", "srs")
        self._influx_bucket = self.config.get("influxdb_bucket", "srsran")
        self._poll_interval = int(self.config.get("poll_interval", 1))

        thread = threading.Thread(target=self._poll_influxdb, daemon=True)
        thread.start()
        print(f"[srsRAN] InfluxDB poller started: {self._influx_url} bucket={self._influx_bucket}", flush=True)

    def _query_sql(self, sql):
        """Query OCUDU's InfluxDB 3 database using SQL."""
        payload = json.dumps({
            "db": self._influx_bucket,
            "q": sql,
            "format": "json",
        }).encode("utf-8")

        request = Request(
            f"{self._influx_url}/api/v3/query_sql",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request, timeout=5) as response:
            return json.load(response)

    def _poll_influxdb(self):
        """Poll OCUDU cell and DU measurements from InfluxDB 3."""
        while True:
            try:
                measurements = {}

                # Get the latest cell measurements
                cell_rows = self._query_sql(
                    "SELECT pci, average_latency FROM cell "
                    "WHERE time >= now() - INTERVAL '30 seconds' "
                    "ORDER BY time DESC LIMIT 1"
                )

                if cell_rows:
                    cell = cell_rows[0]

                    if cell.get("pci") is not None:
                        measurements["pci"] = float(cell["pci"])

                    if cell.get("average_latency") is not None:
                        measurements["cell_average_latency"] = float(
                            cell["average_latency"]
                        )

                # Get the latest MAC performance measurements
                du_rows = self._query_sql(
                    "SELECT du_high_mac_dl_0_cpu_usage_percent, "
                    "du_high_mac_dl_0_average_latency_us "
                    "FROM du "
                    "WHERE time >= now() - INTERVAL '30 seconds' "
                    "AND du_high_mac_dl_0_cpu_usage_percent IS NOT NULL "
                    "ORDER BY time DESC LIMIT 1"
                )

                if du_rows:
                    du = du_rows[0]

                    for field in [
                        "du_high_mac_dl_0_cpu_usage_percent",
                        "du_high_mac_dl_0_average_latency_us",
                    ]:
                        if du.get(field) is not None:
                            measurements[field] = float(du[field])

                # Store the latest observation
                with self._metrics_lock:
                    self._latest_metrics = measurements

                if measurements:
                    print(f"[InfluxDB] Fetched {len(measurements)} fields", flush=True)
                else:
                    print("[InfluxDB] No recent OCUDU measurements", flush=True)

            except Exception as e:
                print(f"[InfluxDB] Error polling: {e}", flush=True)

            sleep(self._poll_interval)

    def poll_measurements(self):
        with self._metrics_lock:
            current = dict(self._latest_metrics)

        if current:
            current["session_id"] = f"session_{self.config['node_id']}_{int(time.time())}"
            return current
        return None


    def _send_ocudu_readonly_command(self, command):
        """Send a read-only command to OCUDU over WebSocket."""

        if command not in ("help", "version"):
            raise ValueError("Only read-only OCUDU commands are permitted")

        url = self.config.get("ocudu_ws_url", "ws://ocudu_gnb:8001")

        ws = websocket.create_connection(url, timeout=5)

        try:
            ws.send(json.dumps({"cmd": command}))
            response = json.loads(ws.recv())
        finally:
            ws.close()

        if not isinstance(response, dict):
            raise ValueError("Invalid OCUDU response")

        if response.get("cmd") != command or "result" not in response:
            raise ValueError("Unexpected OCUDU response")

        return response


    def _validate_rrm_policy(self, policies):
        """Validate the RRM policy before allowing execution."""

        required_fields = {
            "resourceType",
            "rRMPolicyMemberList",
            "min_prb_policy_ratio",
            "max_prb_policy_ratio",
            "dedicated_ratio",
        }

        if set(policies) != required_fields:
            return False

        if policies["resourceType"] != "PRB":
            return False

        members = policies["rRMPolicyMemberList"]

        if not isinstance(members, list) or len(members) != 1:
            return False

        member = members[0]

        if not isinstance(member, dict):
            return False

        if set(member) != {"plmn", "sst", "sd"}:
            return False

        plmn = member["plmn"]

        if (
            not isinstance(plmn, str)
            or len(plmn) not in (5, 6)
            or not plmn.isascii()
            or not plmn.isdigit()
        ):
            return False

        if type(member["sst"]) is not int or not 1 <= member["sst"] <= 255:
            return False

        if type(member["sd"]) is not int or not 0 <= member["sd"] <= 16777215:
            return False

        for field in (
            "min_prb_policy_ratio",
            "max_prb_policy_ratio",
            "dedicated_ratio",
        ):
            value = policies[field]

            if type(value) is not int or not 0 <= value <= 100:
                return False

        if policies["min_prb_policy_ratio"] > policies["max_prb_policy_ratio"]:
            return False

        if policies["dedicated_ratio"] > policies["max_prb_policy_ratio"]:
            return False

        return True


    def _prepare_ocudu_rrm_command(self, payload):
        """Validate and serialise an RRM command without sending it."""

        if not isinstance(payload, dict):
            raise ValueError("Invalid RRM command payload")

        if set(payload) != {"cmd", "policies"}:
            raise ValueError("Unexpected RRM command fields")

        if payload.get("cmd") != "rrm_policy_ratio_set":
            raise ValueError("Unsupported OCUDU command")

        policies = payload.get("policies")

        if not isinstance(policies, dict):
            raise ValueError("Invalid RRM policy")

        if not self._validate_rrm_policy(policies):
            raise ValueError("Invalid RRM policy parameters")

        return json.dumps(payload)


    def _send_ocudu_rrm_command(self, payload):
        """Send a validated RRM command to OCUDU when explicitly enabled."""

        # Validate and prepare the command first
        command = self._prepare_ocudu_rrm_command(payload)

        # Never send live configuration changes by default
        if os.environ.get("OCUDU_RRM_EXECUTION_ENABLED") != "true":
            raise PermissionError("Live OCUDU RRM execution is disabled")

        url = self.config.get("ocudu_ws_url", "ws://ocudu_gnb:8001")

        ws = websocket.create_connection(url, timeout=5)

        try:
            ws.send(command)
            response = ws.recv()
        finally:
            ws.close()

        return response


    def handle_command(self, payload):
        """Recognise RRM commands without changing live OCUDU configuration."""
        print(f"[srsRAN] Processing command: {payload}", flush=True)

        if not isinstance(payload, dict):
            print("[srsRAN] Invalid command payload", flush=True)
            return False

        if payload.get("cmd") != "rrm_policy_ratio_set":
            print("[srsRAN] Unsupported command", flush=True)
            return False

        if set(payload) != {"cmd", "policies"}:
            print("[srsRAN] Unexpected command fields", flush=True)
            return False

        policies = payload.get("policies")
        if not isinstance(policies, dict):
            print("[srsRAN] Invalid RRM policy", flush=True)
            return False

        if policies.get("resourceType") != "PRB":
            print("[srsRAN] Unsupported resource type", flush=True)
            return False

        if not self._validate_rrm_policy(policies):
            print("[srsRAN] Invalid RRM policy parameters", flush=True)
            return False

        if "min_prb_policy_ratio" in policies:
            print(f"[srsRAN] Minimum PRB ratio: {policies['min_prb_policy_ratio']}", flush=True)

        if "max_prb_policy_ratio" in policies:
            print(f"[srsRAN] Maximum PRB ratio: {policies['max_prb_policy_ratio']}", flush=True)

        if "dedicated_ratio" in policies:
            print(f"[srsRAN] Dedicated PRB ratio: {policies['dedicated_ratio']}", flush=True)

        print("[srsRAN] Command recognised - execution disabled", flush=True)
        return False


if __name__ == "__main__":
    NodeRunner().run()

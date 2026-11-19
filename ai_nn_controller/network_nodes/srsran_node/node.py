# Copyright (c) 2026 Trinity College Dublin
#
# This file is dual-licensed:
# - under the AGPL (see LICENSE)
# - under a commercial licence (contact infoknex@tcd.ie)

"""srsRAN Network Node for ai_nn_controller.

Polls InfluxDB for the latest srsRAN metrics (same data source Grafana
uses) and forwards them as measurements through the ai_nn_controller message bus.
"""

from controlled_entity import ControlledEntity, node, NodeRunner
import threading
import time
from time import sleep
import json
from urllib.request import Request, urlopen
import os


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
                    print("[InfluxDB] No recent OCUDU measurements", flush = True)

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


if __name__ == "__main__":
    NodeRunner().run()

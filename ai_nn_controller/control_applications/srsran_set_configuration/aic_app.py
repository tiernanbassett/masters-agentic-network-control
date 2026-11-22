
# Copyright (c) 2026 Trinity College Dublin
#
# This file is dual-licensed:
# - under the AGPL (see LICENSE)
# - under a commercial licence (contact infoknex@tcd.ie)

"""
srsRAN Configuration Control Application.

Validates and submits RRM configuration commands to OCUDU
through the AI-Native Network Controller.

Configuration execution is initially disabled until the
safety and recovery mechanisms have been implemented.
"""

from ai_nn_controller.decorators.aic_app import aic_app
from ai_nn_controller.decorators.command_validator import command_validator
from ai_nn_controller.decorators.agent_controlled import agent_controlled
from ai_nn_controller.AicApp import AicApp
from ai_nn_controller.AicController import AicController
from typing import Optional, Tuple
import argparse

# Import commands module to register specific commands with the framework
import commands


@aic_app(name="SrsranConfig")
class SrsranConfigApp(AicApp):
    """
    Configuration control application for OCUDU.

    Responsible for validating RRM policy configuration requests
    before submitting commands through AI-NNC.
    """

    aic_app_id = 11
    control_loop_update_time = 2

    read_measurements = {}

    # Disabled until configuration execution and rollback are ready
    control_functions = {}

    MIN_PRB_POLICY_RATIO = 0
    MAX_PRB_POLICY_RATIO = 100

    @classmethod
    @command_validator("SET_RRM_POLICY")
    def validate_set_rrm_policy(
        cls, params: dict
    ) -> Tuple[bool, Optional[str]]:
        """Validate an RRM policy configuration request."""

        if not isinstance(params, dict):
            return False, "Configuration parameters must be a dictionary"

        required_fields = [
            "node_id",
            "plmn",
            "sst",
            "sd",
            "min_prb_policy_ratio",
            "max_prb_policy_ratio",
            "dedicated_ratio",
        ]

        for field in required_fields:
            if field not in params:
                return False, f"{field} parameter is required"

        if set(params) != set(required_fields):
            return False, "Unexpected configuration parameters"

        if type(params["node_id"]) is not int or params["node_id"] != 10:
            return False, "Only srsRAN node 10 is supported"

        plmn = params["plmn"]
        if (
            not isinstance(plmn, str)
            or len(plmn) not in (5, 6)
            or not all("0" <= digit <= "9" for digit in plmn)
        ):
            return False, "plmn must be a 5- or 6-digit string"

        if type(params["sst"]) is not int or not 1 <= params["sst"] <= 255:
            return False, "sst must be an integer between 1 and 255"

        if type(params["sd"]) is not int or not 0 <= params["sd"] <= 16777215:
            return False, "sd must be a 24-bit unsigned integer"

        ratio_fields = [
            "min_prb_policy_ratio",
            "max_prb_policy_ratio",
            "dedicated_ratio",
        ]

        for field in ratio_fields:
            value = params[field]

            if type(value) is not int:
                return False, f"{field} must be an integer"

            if not cls.MIN_PRB_POLICY_RATIO <= value <= cls.MAX_PRB_POLICY_RATIO:
                return False, f"{field} must be between 0 and 100"

        if params["min_prb_policy_ratio"] > params["max_prb_policy_ratio"]:
            return False, "Minimum PRB ratio cannot exceed maximum PRB ratio"

        if params["dedicated_ratio"] > params["max_prb_policy_ratio"]:
            return False, "Dedicated PRB ratio cannot exceed maximum PRB ratio"

        # These checks establish basic input validity, not full safety.
        # Approved slices, checkpointing, and execution preconditions
        # must be verified before enabling configuration changes.
        return True, None

    @classmethod
    def process(cls, measurements):
        """Periodic processing for the configuration application."""
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="srsRAN Configuration Control Application"
    )
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--port", "-p", type=int, default=8000)
    parser.add_argument("--host", type=str, default="0.0.0.0")
    args = parser.parse_args()

    AicController(
        with_api=True,
        api_host=args.host,
        api_port=args.port,
        verbose=args.verbose
    ).run()

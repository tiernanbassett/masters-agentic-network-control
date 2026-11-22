
# Copyright (c) 2026 Trinity College Dublin
#
# This file is dual-licensed:
# - under the AGPL (see LICENSE)
# - under a commercial licence (contact infoknex@tcd.ie)

"""
Command Definitions for srsRAN Configuration.

This module defines commands for configuring OCUDU through AI-NNC.
Commands are registered with the ai_nn_controller framework.

To add a new command:
1. Define a handler function that takes (node_id, value) and returns JSON
2. Define the JSON schema for the command parameters
3. Register the command using register_specific_commands()
"""

import json
from ai_nn_controller.registry import register_command


# =============================================================================
# Command Handlers
# =============================================================================

def set_rrm_policy_handler(node_id: int, value: dict) -> str:
    """
    Handle SET_RRM_POLICY command for OCUDU.

    Transforms AI-NNC command parameters into the JSON format
    expected by OCUDU's rrm_policy_ratio_set WebSocket command.

    Args:
        node_id: Target node ID (10 for srsRAN)
        value: {
            "plmn": str,
            "sst": int,
            "sd": int,
            "min_prb_policy_ratio": int,
            "max_prb_policy_ratio": int,
            "dedicated_ratio": int
        }

    Returns:
        JSON string payload for OCUDU
    """
    if type(node_id) is not int or node_id != 10:
        raise ValueError("SET_RRM_POLICY only supports node 10")

    if not isinstance(value, dict):
        raise ValueError("Command value must be a dictionary")

    required_fields = [
        "plmn",
        "sst",
        "sd",
        "min_prb_policy_ratio",
        "max_prb_policy_ratio",
        "dedicated_ratio",
    ]

    for field in required_fields:
        if field not in value:
            raise ValueError(f"Missing required parameter: {field}")

    if (not isinstance(value["plmn"], str)
            or not value["plmn"].isdigit()
            or len(value["plmn"]) not in (5, 6)):
        raise ValueError("plmn must be a 5- or 6-digit string")

    for field in required_fields[1:]:
        if type(value[field]) is not int:
            raise ValueError(f"{field} must be an integer")

    if not 1 <= value["sst"] <= 255:
        raise ValueError("sst must be between 1 and 255")

    if not 0 <= value["sd"] <= 16777215:
        raise ValueError("sd must be a 24-bit unsigned integer")

    for field in (
        "min_prb_policy_ratio",
        "max_prb_policy_ratio",
        "dedicated_ratio",
    ):
        if not 0 <= value[field] <= 100:
            raise ValueError(f"{field} must be between 0 and 100")

    payload = {
        "cmd": "rrm_policy_ratio_set",
        "policies": {
            "resourceType": "PRB",
            "rRMPolicyMemberList": [
                {
                    "plmn": value["plmn"],
                    "sst": value["sst"],
                    "sd": value["sd"],
                }
            ],
            "min_prb_policy_ratio": value["min_prb_policy_ratio"],
            "max_prb_policy_ratio": value["max_prb_policy_ratio"],
            "dedicated_ratio": value["dedicated_ratio"],
        },
    }

    return json.dumps(payload)


# =============================================================================
# Command Schemas (for MCP tool generation)
# =============================================================================

SET_RRM_POLICY_SCHEMA = {
    "description": "Configure OCUDU RRM PRB allocation ratios",
    "properties": {
        "node_id": {
            "type": "integer",
            "enum": [10],
            "description": "Target srsRAN node ID"
        },
        "plmn": {
            "type": "string",
            "pattern": "^[0-9]{5,6}$",
            "description": "Target network PLMN identifier"
        },
        "sst": {
            "type": "integer",
            "minimum": 1,
            "maximum": 255,
            "description": "Slice/Service Type"
        },
        "sd": {
            "type": "integer",
            "minimum": 0,
            "maximum": 16777215,
            "description": "Slice Differentiator"
        },
        "min_prb_policy_ratio": {
            "type": "integer",
            "minimum": 0,
            "maximum": 100,
            "description": "Minimum PRB allocation percentage"
        },
        "max_prb_policy_ratio": {
            "type": "integer",
            "minimum": 0,
            "maximum": 100,
            "description": "Maximum PRB allocation percentage"
        },
        "dedicated_ratio": {
            "type": "integer",
            "minimum": 0,
            "maximum": 100,
            "description": "Dedicated PRB allocation percentage"
        }
    },
    "required": [
        "node_id",
        "plmn",
        "sst",
        "sd",
        "min_prb_policy_ratio",
        "max_prb_policy_ratio",
        "dedicated_ratio"
    ]
}


# =============================================================================
# Register Commands with Framework
# =============================================================================

def register_specific_commands():
    """Register srsRAN configuration commands with AI-NNC."""

    register_command(
        name="SET_RRM_POLICY",
        handler=set_rrm_policy_handler,
        schema=SET_RRM_POLICY_SCHEMA
    )


# Explicit capability metadata for plugin-style registration
COMMAND_CAPABILITIES = [
    "SET_RRM_POLICY",
]


def get_command_capabilities() -> list[str]:
    """Return command capability names exposed by this application."""
    return list(COMMAND_CAPABILITIES)

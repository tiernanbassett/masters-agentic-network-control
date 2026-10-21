# Design Choices

This file includes some reasoning around design choices

## AI-NNC

Using AI-NNC: Modular, open source, flexible, supports MCP

Alternatives: ORAN-RIC - no built-in MCP support, requires more work to add agent

In the AI-NNC there is an srsRAN node but it only sends measurements, could come up with some way to issue commands using handle_command()?

## OCUDU

OCUDU to issue commands: Open source, supports changin resource block allocation policies over a wireless network

Alternatives: TBD

Potential parameters: tx power, resource block allocation, scheduling

## Evaluation

Evaluation: Could compare agent to optimisation algorithms, baselines etc.
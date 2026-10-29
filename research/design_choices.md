# Design Choices

This file includes some reasoning around design choices

## AI-NNC

Using AI-NNC: Modular, open source, flexible, supports MCP

Alternatives: ORAN-RIC - no built-in MCP support, requires more work to add agent

In the AI-NNC there is an srsRAN node but it only sends measurements, could come up with some way to issue commands using handle_command()?

## Controller Comparison
Found example RICs for OCUDU, flexRIC and ORAN SC RIC. Unsure on how to adapt AI-NNC to issue commands to OCUDU, needs more research. Possible API?, FlexRIC and ORAN SC RIC could be used as a bridge? But dont know about the added complexity.

## OCUDU

OCUDU to issue commands: Open source, supports changin resource block allocation policies over a wireless network

Alternatives: TBD

Potential parameters: tx power, resource block allocation, scheduling

## Evaluation

Evaluation: Could compare agent to optimisation algorithms, baselines etc.

## Agent Harness
OpenClaw(existing environment, schedulers)
Hermes(existing environment, schedulers)
OpenCode(existing environment) 
LangGraph(persistent states, straightforward workflow that must be followed)
OpenAI SDK (session saving, built in loop)

LangGraph more programmable but more work required then. Others dont have as explicit a flow and may require more work to implement the exact loop i want.
So depends if I want to program more of an environment or more of a structure, not sure which is better and which is more work.
# A Survey on Large Language Model Based Autonomous Agents

**Author:** Wang et al.

**Description:** A survey paper discussing the construction, applications, and evaluation methods of LLM-based agents.

## Notes

### Agent Construction

- Planning
- Memory
- Profile
- Action

### Relevance to My Dissertation

- **Planning:** May have to be minimised due to latency (will investigate).
- **Memory:** Both long-term and short-term memory — trade-off.
- **Profile:** Simple, objective.
- **Action:** Interaction with network controller.

### Applications

There are many applications. Mine is an engineering-type application that is time-bound.

### Evaluation of Agents

- **Subjective:** With humans.
- **Objective:** Predefined metrics, but benchmarks are needed.

### Challenges

Challenges include hallucinations, knowledge boundaries, and latency.

Latency is a big consideration in my dissertation.

### Critical Analysis

Good foundational understanding of agentic AI. Need more thorough research, particularly related to network control (will definitely look at AI-native networking).

# 6G Needs Agents: Toward Agentic AI-Native Networks for Autonomous Intelligence

**Author:** Ferrag et al. (2026)

**Description:** A research paper proposing an agentic AI-native 6G network architecture and evaluating different LLM configurations.

## Notes

### Existing AI-Native Networking
As 6G Networks become more heterogenous, the optimisation-centric nature of current algorithms become too narrow-minded and may be insufficient. This leaves room for a high-level decision layer on top of the contoller.

### Proposed Architecture
Infrastructure provides measurements to a semantic layer and exposes parameters available while perfoming operations, semantic layer gets the context and uses the objectives to pass up to the reasoning layer which makes a decision on what configurations to propose. Top layer coordinates multiple agents across different domains.

### Relevance to My Dissertation
The seperation between reasoning and deterministic actions is something that would be relevant to the agent and the AI-Native Network COntroller, letting the controller have guardrails etc. to protect the network from hallucinations and detrimental configurations .

### Experimental Evaluation
The author used a few thousand MCQs and mutliple models, noting their accuracy and their latency. 

### Findings
They found a tradeoff between computational capability, latency and accuracy, this is particularly relevant to our loop as the agent will need to be accurate enough to be good but quick enough too.

### Challenges
Obvious risks, hallucinations, context poisoning, safety

### Critical Analysis
They did not use an actual loop simulation, and didn't compare to a baseline deterministic model. They mainly compared different LLMs.
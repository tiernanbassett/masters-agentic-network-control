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
Obvious risks, hallucinations, context poisoning, safety, need for some coordination between agents

### Critical Analysis
They did not use an actual loop simulation, and didn't compare to a baseline deterministic model. They mainly compared different LLMs.

# Understanding O-RAN: Architecture, Interfaces, Algorithms, Security, and Research Challenges

**Author:** Polese et al. (2023)

**Description:** A survey and tutorial examining O-RAN architecture, interfaces, intelligent network control, and research challenges.

## Notes

### Existing Wireless Network Architecture
Traditional networks were sold to network operators as unconfigurable black boxes. This limits interpoerability and coordination between nodes and can leave someone stuck with the same vendor. (vendor lock-in)

### O-RAN Architecture
O-RAN is a modular version of this with seperate components, open interfaces for configurability, and intelligent controllers (slower (non RT RIC) which hosts rApps, and fast (near RT RIC) which hosts xApps). An RIC may control a group of network nodes.

### Intelligent Network Control
An xApp takes in measurments(KPMs) and uses them. These KPIs effect its action. It controllers network components using an E2 interface, which is standardised to allow compatibility between the controller and the nodes. rApps take longer and make longer term decisions such as policies, which are communicated to Near RT RIC using an A1 interface. 

### Relevance to My Dissertation
Like rApps, an agent can operate at a higher level if the latency isn't sufficient enough for xApps actions. The architecture of a closed loop control with post-action safety mechanisms is something that could inspire an agentic control loop in a network.

### Challenges and Limitations
Indirect conflicts can occur when two xApps configure parameters that aren't exactly conflicting but can cause a degradation when coupled. This can go undetected and allows room for testing a mechanism to mitigate this, for example, an AI agent.

### Critical Analysis
No direct demonstration that AI control with RIC performs better than traditional optimisation, but lists all of the features added or upgraded from traditional networks.

# Scheduling Algorithms for 5G Networks and Beyond: Classification and Survey

**Author:** Mamane et al. (2022)

**Description:** A survey paper examining radio resource allocation and scheduling algorithms in 5G networks.

## Notes

### Radio Resource Management and Scheduling
Radio resources are broken up into reource blocks, which are 2D blocks of time and bandwidth. The base station uses schedulers to hand out these resource blocks. There are mutliple algorithms of varying complexity, different algorithms consider different metrics and prioritise different things. These include Proportional Fair and Round Robin.

### Scheduling Algorithms
These vary in complexity and take into account different things such as channel quality, average throughput etc. Round robin is totally fair, PF takes CQI and avg throughput into account, best CQI always prioritises the best channel quality.

### Factors Influencing Scheduling Decisions
CQI, average throughput, user's needs (URLLC, eMBB, mMTC), buffer size, HOL delay

### Performance Evaluation Metrics
throughput (data/time), goodput (data-overhead/time), latency, spectral efficiency(bps/bandwidth), fairnes, packet loss ration

### Machine Learning-Based Scheduling
ML-based scheduling uses ML models to try to optimise scheduling based on multiple metrics adn objectives. In hopes it is more accurate/true to what the operator wants. They are more complex generally and take more computational time.

### Relevance to My Dissertation
This shows that different network objectives need different strategies. Agentic AI may deal well with this flexibility and high-level objectives. Algorithms like these may be used as baselines.

### Challenges and Limitations
Tradeoff between throughput and fairness when scheduling. Can't have always perfect conditions for everyone. Some algorithms while better may add additional complexity (this may be relevant to my agent).

### Critical Analysis
This survey explains different types of scheduling, some advanced ones, the metrics schedulers use and how resources are allocated. No experiments however if I need to make one I can use something from here as a baseline.
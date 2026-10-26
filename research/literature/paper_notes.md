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

# Towards Closed-loop Automation in 5G Open RAN: Coupling an Open-Source Simulator with xApps

**Author:** Karamplias et al. (2022)

**Description:** A paper that demonstrates closed loop automation using an RL-based controller to optimise power and throughput.

## Notes

### Closed-Loop Control Architecture
Two xApps operating using the Near-RT RIC. xApp 1 generating measurements and xApp 2 containing the DRL-based algorithms. Controller can switch between different pretrained algorithms depending on objective. Process repeats creating a loop.

### Experimental Evaluation
Controller was compared to an average transmission power controller. Results demonstrated generall better throughput and network performance, but omitted latency and computational complexity.

### Relevance to My Dissertation
Potentially I can use the same loop idea for the agent, this also gives a baseline for me to compare to.

### Challenges and Limitations
There's no post-action safety guardrails (such as checkpointing) mentioned in the paper, and as already identified the latency and computational complexity isn't included in their experimental comparison.

### Critical Analysis
The paper successfully shows that this is possible and you can get good results, but doesn't give enough evidence with regards to post-action safety or complexity/latency for it to be deployed as a real network controller. I'd imagine my agent may have the same limitations.

# AI-Native Network Controller: A Modular Framework for Safe Agentic Control of Multi-Domain Network Infrastructure

**Author:** Dzaferagic (2026)

**Description:** A research paper presenting an open-source, modular AI-native network controller designed to support safe agentic control across multiple network domains.

## Notes

### Existing Network Controllers
- Existing Controllers are generally domain-specific, and as networks become more hetergeneous, the ability to control across domains becomes essential. Existing controllers also lack support for Agentic AI across domains.

### Proposed AI-NNC Architecture
- **Control Plane:** Includes the apps that can offer configurations and read measurements, as well as the MCP server for the agent.
- **Registration Plane:** Including a registration of all apps and nodes in the network. Also keeps track of which measurements and commands are available.
- **Data Plane:** Includes a ZeroMQ message broker which sends data between nodes adn apps. 

### Network Node Integration
- Nodes are connected to the controller via adapters which act as middlemen between the nodes and the controller. These node adapters can handle setup, sending measurements, and applying configurations.

### Control Applications and MCP
- Applications include different commands which can be used on different nodes. There are @agent_controlled ones too which allow agents to invoke them as tools using an MCP server.

### Safety Guardrails and Command Validation
- There is a command validator (given by @command_validator) used to ensure that any command issued from an app, whether it be issued by an agent or not, does not go over or under a max/min threshold for a parameter. This essentially acts as a safety gaurdrail. This does not however stop a command from worsening network performance.

### Conflict Detection
- The controller also detects when two apps will conflict, this also includes indirect conflicts. This is detected in the registration plane which keeps track of what apps issue commands to what nodes. The conflict mitigator in the plane mitigates the conflict arbitrates the conflict.

### Experimental Evaluation
- Controller validated with both simulated and physical optical equipment

### Relevance to My Dissertation
- Using this controller may be valuable to my project as it is flexible, already includes pre-action safety with the command validator, and already enables MCP for an agent. It is also open source and there is good documentation on it. The paper even notes that it can be paired with other controllers such as O-RAN Near-RT RIC

### Challenges and Limitations
- I think for adding an agent to this a loop needs to be added, along with post-action validation. This includes checkpointing and rollback, as even with satefy guardrails an agent may decrease performance.

### Critical Analysis
- This is a promising contender for a controller to use for an AI agent, however more research into alternatives is needed.

# ReAct: Synergizing Reasoning and Acting in Language Models

**Author:** Yao et al. (2023)

**Description:** Paper demonstrating the ReAct framework, where LLMs combine reasoning and acting to produce better and more accurate results

## Notes

### ReAct Architecture
An LLM observes from its environment, reasons about what it observed, and then acts based on its reasoning, it can then observe again to create a loop.

### Experimental Evaluation
ReAct was compared against CoT (just reasoning) and Act using different benchmarks such as HotPotQA and ALFWorld, this involved desicion making and fact verification.

### Findings
It outperformed the alternatives almost all of the time, CoT outperformed it on HotPotQA, prompting the authors to combine the two and outperform both of them.

### Relevance to My Dissertation
This framework would work well for my agrentic loop as it reduces hallucinations and helps with decision making. The authors specify too that reasoning doesn't have to occur on every step for good results, which may help with the issue of latency.

### Challenges and Limitations
One limitation is latency, for example, in a fast-paced environment the LLM may be reasoning over expired measurements form its observation, leading to multiple wrong actions. There is also still issues with repeptitive incorrect actions or wrong though processes.

### Critical Analysis
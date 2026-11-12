
import json
from typing import TypedDict
from urllib.request import Request, urlopen
import operator
from typing import Annotated
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    measurements: dict | None
    history: Annotated[list[dict], operator.add]
    last_decision: dict | None
    decision_history: Annotated[list[dict], operator.add]
    last_execution: dict | None
    execution_history: Annotated[list[dict], operator.add]
    iterations_remaining: int


def read_measurements(state: AgentState):
    payload = {
        "name": "SrsranReader_get_ue_summary",
        "arguments": {}
    }

    request = Request(
        "http://localhost:8000/mcp/tools/call",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urlopen(request, timeout=10) as response:
        data = json.load(response)

    if not data.get("success"):
        raise RuntimeError(f"Tool call failed: {data}")

    observation = data["result"]["result"]

    if observation.get("status") != "ok":
        raise RuntimeError(f"No valid observation: {observation}")

    return {
        "measurements": observation,
        "history": [observation],
    }

def make_decision(state: AgentState):
    bler = state["measurements"]["ue_metrics"]["dl_bler"]

    if bler is None:
        action = "insufficient_data"
    elif bler > 0.10:
        action = "investigate_high_bler"
    else:
        action = "maintain_configuration"

    decision = {
        "action": action,
        "status": "proposed",
        "dl_bler": bler,
        "observation_number": len(state["history"])
    }

    return {
        "last_decision": decision,
        "decision_history": [decision]
    }

def execute_decision(state: AgentState):
    decision = state["last_decision"]
    action = decision["action"]

    if action == "insufficient_data":
        status = "skipped"
    elif action == "investigate_high_bler":
        status = "investigation"
    elif action == "maintain_configuration":
        status = "no_change"
    else:
        raise ValueError(f"Unknown action: {action}")

    execution = {
        "action": action,
        "execution_status": status,
        "observation_number": decision["observation_number"]
    }

    return {
        "last_execution": execution,
        "execution_history": [execution],
        "iterations_remaining": state["iterations_remaining"] - 1
    }

def continue_loop(state: AgentState):
    if state["iterations_remaining"] > 0:
        return "observe"
    else:
        return "end"

graph = StateGraph(AgentState)
graph.add_node("observe", read_measurements)
graph.add_node("decide", make_decision)
graph.add_node("execute", execute_decision)
graph.add_edge(START, "observe")
graph.add_edge("observe", "decide")
graph.add_edge("decide", "execute")
graph.add_conditional_edges(
    "execute",
    continue_loop,
    {
        "observe": "observe",
        "end": END
    }
)

config = {
    "configurable": {
        "thread_id": "network-control-decide-1"
    }
}

with SqliteSaver.from_conn_string("agent_checkpoints.sqlite") as checkpointer:
    agent = graph.compile(checkpointer=checkpointer)

    first = agent.invoke(
        {"measurements": None, "history": [], "iterations_remaining":2},
        config
    )

    second = agent.invoke(
        {"measurements": None, "iterations_remaining":2},
        config
    )

print("Stored observations:", len(second["history"]))
print("Latest observation:", second["measurements"])
print("Iterations remaining:", second["iterations_remaining"])
print("Last decision:", second["last_decision"])
print("Stored decisions:", len(second["decision_history"]))
print("Last execution:", second["last_execution"])
print("Stored executions:", len(second["execution_history"]))
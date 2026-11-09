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


graph = StateGraph(AgentState)
graph.add_node("observe", read_measurements)
graph.add_edge(START, "observe")
graph.add_edge("observe", END)

config = {
    "configurable": {
        "thread_id": "network-control-1"
    }
}

with SqliteSaver.from_conn_string("agent_checkpoints.sqlite") as checkpointer:
    agent = graph.compile(checkpointer=checkpointer)

    first = agent.invoke(
        {"measurements": None, "history": []},
        config
    )

    second = agent.invoke(
        {"measurements": None},
        config
    )

    print("Stored observations:", len(second["history"]))
    print(json.dumps(second["history"], indent=2))
from langgraph.graph import START, StateGraph
from typing import TypedDict


class SubgraphState(TypedDict):
    foo: str
    bar: str


def subgraph_node_1(state: SubgraphState):
    return {"bar": "bar"}


def subgraph_node_2(state: SubgraphState):
    return {"foo": state["foo"] + state["bar"]}


subgraph_builder = StateGraph(SubgraphState)
subgraph_builder.add_node(subgraph_node_1)
subgraph_builder.add_node(subgraph_node_2)
subgraph_builder.add_edge(START, "subgraph_node_1")
subgraph_builder.add_edge("subgraph_node_1", "subgraph_node_2")
subgraph = subgraph_builder.compile()


class ParentState(TypedDict):
    foo: str


def node_1(state: ParentState):
    return {"foo": "hi!" + state["foo"]}


build = StateGraph(ParentState)
build.add_node("node_1", node_1)
build.add_node("node_2", subgraph)
build.add_edge(START, "node_1")
build.add_edge("node_1", "node_2")
graph = build.compile()

for chunk in graph.stream(
        {"foo": "foo"},
        stream_mode="updates",
        subgraphs=True
):
    print(chunk)

from langgraph.graph import StateGraph, END
from app.agent_state import AgentState
from app.agent_nodes import (
    extract_node,
    decision_node,
    sales_node,
    non_sales_node
)

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("extract", extract_node)
    graph.add_node("decide", decision_node)
    graph.add_node("sales", sales_node)
    graph.add_node("non_sales", non_sales_node)

    graph.set_entry_point("extract")

    graph.add_edge("extract", "decide")

    graph.add_conditional_edges(
        "decide",
        lambda state: state["decision"],
        {
            "sales": "sales",
            "non_sales": "non_sales"
        }
    )

    graph.add_edge("sales", END)
    graph.add_edge("non_sales", END)

    return graph.compile()

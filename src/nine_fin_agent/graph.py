from langgraph.graph import MessagesState, StateGraph, END
from langgraph.prebuilt import tools_condition
from langgraph.checkpoint.memory import MemorySaver

from src.nine_fin_agent.node import \
    query_or_respond,tools,generate

MEMORY = MemorySaver()

def build_graph():
    graph_builder = StateGraph(MessagesState)
    graph_builder.add_node(query_or_respond)
    graph_builder.add_node(tools)
    graph_builder.add_node(generate)

    graph_builder.set_entry_point("query_or_respond")
    graph_builder.add_conditional_edges(
        "query_or_respond",
        tools_condition,
        {END: END, "tools": "tools"},
    )
    graph_builder.add_edge("tools", "generate")
    graph_builder.add_edge("generate", END)
    graph = graph_builder.compile(checkpointer=MEMORY)
    return graph

graph = build_graph()


#if __name__ == "__main__":
#    input_message = "Tronox Sales 2023?"
#    for step in graph.stream(
#            {"messages": [{"role": "user", "content": input_message}]},
#            stream_mode="values",
#    ):
#        step["messages"][-1].pretty_print()


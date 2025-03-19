from typing import Annotated
from langchain_ollama.chat_models import ChatOllama

from typing_extensions import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages

from langgraph.graph import END, START


class CustomState(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(CustomState)


llm = ChatOllama(
    model="gemma3:4b",
    temperature=0.0,
)


def chatbot(state: CustomState):
    return {"messages": [llm.invoke(state["messages"])]}


# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()


if __name__ == "__main__":
    graph.invoke({"messages": [{"role": "user", "content": "안녕?"}]})
    print(graph.invoke({"messages": [{"role": "user", "content": "안녕?"}]})["messages"][-1].content)

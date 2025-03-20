from typing import Annotated

from langchain_core.prompts import PromptTemplate
from langchain_ollama.chat_models import ChatOllama
from typing_extensions import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_core.prompts import PromptTemplate, ChatPromptTemplate


class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)

llm = ChatOllama(model="gemma3:4b")

def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=[tool])
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
# Any time a tool is called, we return to the chatbot to decide the next step
graph_builder.add_edge("tools", "chatbot")
graph_builder.set_entry_point("chatbot")
graph = graph_builder.compile()

if __name__ == "__main__":
    graph.invoke({"messages": [{"role": "user", "content": "안녕?"}]})
    print(graph.invoke({"messages": [{"role": "user", "content": "안녕?"}]})["messages"][-1].content)




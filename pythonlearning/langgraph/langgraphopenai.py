from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os

load_dotenv()
llm_api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = llm_api_key

llm = init_chat_model("openai:gpt-4.1")

class State(TypedDict):
    messages: Annotated[list, add_messages] 

def chatbot(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


graph = StateGraph(State)
graph.add_node("chatbot", chatbot)
graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)

app = graph.compile()

user_input= input("You: ")
output = app.invoke({"messages": [{"role": "user", "content": user_input}]})
print(output)





# langgraph_agent.py
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langgraph.graph import StateGraph, END

# ---- Setup retriever ----
CHROMA_DIR = "./chroma_db"
emb = OpenAIEmbeddings()
vectordb = Chroma(
    collection_name="my_docs",
    persist_directory=CHROMA_DIR,
    embedding_function=emb,
)
retriever = vectordb.as_retriever(search_kwargs={"k": 4})

# ---- Models ----
decision_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
answer_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# ---- Define State ----
class AgentState(dict):
    query: str
    decision: str
    context: str
    answer: str

# ---- Graph steps ----
def decide(state: AgentState):
    q = state["query"]
    prompt = f"""Question: {q}
Decide if retrieval is needed.
Return only 'RETRIEVE' or 'ANSWER'."""
    resp = decision_llm.invoke(prompt)
    state["decision"] = resp.content.strip().upper()
    return state

def retrieve(state: AgentState):
    if state["decision"] == "RETRIEVE":
        docs = retriever.get_relevant_documents(state["query"])
        context = "\n\n".join([d.page_content for d in docs])
        state["context"] = context
    else:
        state["context"] = ""
    return state

def answer(state: AgentState):
    if state["context"]:
        prompt = f"""Use the context below to answer:
Context:
{state['context']}

Question: {state['query']}
Answer:"""
    else:
        prompt = f"Answer directly: {state['query']}"
    resp = answer_llm.invoke(prompt)
    state["answer"] = resp.content
    return state

# ---- Build Graph ----
graph = StateGraph(AgentState)
graph.add_node("decide", decide)
graph.add_node("retrieve", retrieve)
graph.add_node("answer", answer)

graph.set_entry_point("decide")
graph.add_edge("decide", "retrieve")
graph.add_edge("retrieve", "answer")
graph.add_edge("answer", END)

agent = graph.compile()

if __name__ == "__main__":
    q = input("Q: ")
    result = agent.invoke({"query": q})
    print("A:", result["answer"])

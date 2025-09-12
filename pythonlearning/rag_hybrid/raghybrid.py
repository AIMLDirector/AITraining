import os
from typing import List, Tuple
from dataclasses import dataclass
from dotenv import load_dotenv

# --- OpenAI (latest SDK) ---
from openai import OpenAI

# --- LangChain base ---
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# --- Loaders, splitters, embeddings, vector store ---
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS

# --- Web search (Tavily) ---
from langchain_community.tools.tavily_search import TavilySearchResults

# --- Utilities ---
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
assert OPENAI_API_KEY, "Missing OPENAI_API_KEY"
assert TAVILY_API_KEY, "Missing TAVILY_API_KEY"

# Initialize clients
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)  # fast, cheap; swap to gpt-4.1 for best quality
client = OpenAI(api_key=OPENAI_API_KEY)

# ---------- Ingestion & Indexing ----------

def load_local_corpus(data_dir: str = "data") -> List[Document]:
    """
    Loads PDFs and text-like files from data_dir.
    """
    docs: List[Document] = []

    # PDFs
    pdf_loader = DirectoryLoader(
        data_dir,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
        show_progress=True
    )
    docs += pdf_loader.load()

    # Text-like files
    txt_loader = DirectoryLoader(
        data_dir,
        glob="**/*.txt",
        loader_cls=TextLoader,
        show_progress=True
    )
    # Filter out PDFs already covered; keep .md .txt .rst .json .yaml etc.
    for d in txt_loader.load():
        if not d.metadata.get("source", "").lower().endswith(".pdf"):
            docs.append(d)

    return docs

def chunk_documents(docs: List[Document], chunk_size=1000, chunk_overlap=150) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True
    )
    return splitter.split_documents(docs)

def build_or_load_faiss_index(chunks: List[Document], index_dir: str = "faiss_index") -> FAISS:
    embeddings = OpenAIEmbeddings()  # uses text-embedding-3-large by default if set, else 3-small; can pass model="text-embedding-3-large"
    if os.path.isdir(index_dir):
        vs = FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)
    else:
        vs = FAISS.from_documents(chunks, embeddings)
        vs.save_local(index_dir)
    return vs

# ---------- Web Search Retriever (Tavily) ----------
# We’ll wrap Tavily tool to return LangChain Documents
tavily_tool = TavilySearchResults(max_results=5, include_answers=True)

def web_search_docs(query: str) -> List[Document]:
    """
    Runs Tavily search and returns results as Documents with source links in metadata.
    """
    results = tavily_tool.invoke({"query": query})
    docs = []
    for r in results:
        # r has 'title', 'url', 'content' (snippet), maybe 'score'
        content = r.get("content") or ""
        if not content:
            continue
        docs.append(
            Document(
                page_content=content,
                metadata={
                    "title": r.get("title", ""),
                    "source": r.get("url", ""),
                    "retriever": "web:tavily"
                }
            )
        )
    return docs

# ---------- Hybrid Retrieval Logic ----------
@dataclass
class Retrieved:
    local_docs: List[Document]
    web_docs: List[Document]

def hybrid_retrieve(query: str, vs: FAISS, k_local: int = 4, k_web: int = 4) -> Retrieved:
    """
    Retrieve from local FAISS and web, then return both sets.
    Simple rule: always combine to create broader context with sources.
    You can add gating (e.g., only web if local low score).
    """
    local_docs = vs.similarity_search(query, k=k_local)
    web_docs   = web_search_docs(query)[:k_web]
    return Retrieved(local_docs=local_docs, web_docs=web_docs)

# Optional: a super-lightweight post-retrieval *re-rank* using the LLM itself.
RERANK_PROMPT = ChatPromptTemplate.from_template(
    """You are a helpful research assistant. 
You will receive a user question and N context chunks. 
Rank the chunks by how useful they are for answering the question. 
Return the top {top_k} chunk indices (0-based) as a comma-separated list ONLY.

Question: {question}

Chunks:
{chunks}
"""
)

def rerank_with_llm(question: str, docs: List[Document], top_k: int = 6) -> List[Document]:
    # Build a numbered list for the model
    numbered = []
    for i, d in enumerate(docs):
        snippet = d.page_content[:1200]
        numbered.append(f"[{i}] {snippet}")
    ranked = RERANK_PROMPT | llm | StrOutputParser()
    indices_str = ranked.invoke({"question": question, "chunks": "\n\n".join(numbered), "top_k": top_k})
    # Parse indices
    keep = []
    for token in indices_str.replace(" ", "").split(","):
        if token.isdigit():
            idx = int(token)
            if 0 <= idx < len(docs):
                keep.append(docs[idx])
    # Deduplicate while preserving order
    seen = set()
    uniq = []
    for d in keep:
        key = (d.metadata.get("source", ""), d.metadata.get("retriever", ""), d.page_content[:50])
        if key not in seen:
            seen.add(key)
            uniq.append(d)
    return uniq or docs[:top_k]

# ---------- Compose final answer with sources ----------
ANSWER_PROMPT = ChatPromptTemplate.from_template(
    """You are a precise assistant. Use the context to answer the user's question.
- Cite sources inline like [local:filename] or [web:domain] right after claims derived from them.
- If you are unsure, say so and suggest next steps.
- Keep the answer concise but complete.

Question: {question}

Context:
{context}

Now answer:
"""
)

def format_citation(md: dict) -> str:
    if md.get("retriever") == "web:tavily":
        src = md.get("source", "")
        domain = src.split("/")[2] if "://" in src else src
        return f"[web:{domain}]"
    # local file
    src = md.get("source", "")
    fname = os.path.basename(src) if src else "local"
    return f"[local:{fname}]"

def docs_to_context(docs: List[Document]) -> str:
    lines = []
    for d in docs:
        cite = format_citation(d.metadata)
        lines.append(f"{cite} {d.page_content}")
    return "\n\n".join(lines)

def answer_question(query: str, vs: FAISS) -> Tuple[str, List[Document]]:
    retrieved = hybrid_retrieve(query, vs)
    # Merge, then re-rank for relevance
    merged = retrieved.local_docs + retrieved.web_docs
    reranked = rerank_with_llm(query, merged, top_k=8)

    prompt = ANSWER_PROMPT | llm | StrOutputParser()
    response = prompt.invoke({
        "question": query,
        "context": docs_to_context(reranked)
    })
    return response, reranked

# ---------- Main (build index once, then chat loop) ----------
def ensure_index(index_dir="faiss_index") -> FAISS:
    if os.path.isdir(index_dir):
        embeddings = OpenAIEmbeddings()
        return FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)
    print("Building index from ./data ...")
    docs = load_local_corpus("data")
    chunks = chunk_documents(docs)
    return build_or_load_faiss_index(chunks, index_dir=index_dir)

if __name__ == "__main__":
    vectorstore = ensure_index()

    print("Hybrid RAG ready! Type a question (or 'exit'):")
    while True:
        q = input("\n> ")
        if q.strip().lower() in {"exit", "quit"}:
            break
        try:
            ans, used_docs = answer_question(q, vectorstore)
            print("\n--- Answer ---\n")
            print(ans)
            print("\n--- Sources ---")
            for d in used_docs:
                r = d.metadata.get("retriever", "local")
                s = d.metadata.get("source", "")
                print(f"- {r} :: {s}")
        except Exception as e:
            print("Error:", e)

import pickle
import faiss
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
import numpy as np
from promptflow.tracing import start_trace

from opentelemetry import trace
from opentelemetry.instrumentation.langchain import LangchainInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

# Start Promptflow tracing and configure OpenTelemetry
start_trace()
LangchainInstrumentor().instrument()

# Get a tracer for manual instrumentation
tracer = trace.get_tracer(__name__)

# Configure a console span exporter to view logs in the terminal
span_exporter = ConsoleSpanExporter()
tracer_provider = trace.get_tracer_provider()
tracer_provider.add_span_processor(SimpleSpanProcessor(span_exporter))

# --- Configuration ---
MODEL_NAME = "all-MiniLM-L6-v2"
INDEX_SAVE_PATH = "models/faiss_index.pkl"
CHUNKS_SAVE_PATH = "models/docs_chunks.pkl"

# --- 1. Load Pre-trained Index and Chunks ---
print("Loading Faiss index and document chunks...")
with tracer.start_as_current_span("load_faiss_index") as span:
    with open(INDEX_SAVE_PATH, "rb") as f:
        faiss_index = pickle.load(f)
    span.set_attribute("index.path", INDEX_SAVE_PATH)

with tracer.start_as_current_span("load_document_chunks") as span:
    with open(CHUNKS_SAVE_PATH, "rb") as f:
        docs_chunks = pickle.load(f)
    span.set_attribute("chunks.path", CHUNKS_SAVE_PATH)

# --- 2. Initialize the Embedding Model ---
embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)

def retrieve_and_generate(query, k=3):
    """
    Performs the RAG process: retrieves relevant docs and generates a response.
    """
    with tracer.start_as_current_span("retrieve_and_generate_query") as span:
        span.set_attribute("user.query", query)

        # --- 3. Embed the Query ---
        with tracer.start_as_current_span("embed_query"):
            query_embedding = embeddings.embed_query(query)
            query_embedding_np = np.array([query_embedding]).astype("float32")

        # --- 4. Similarity Search (Faiss) ---
        with tracer.start_as_current_span("faiss_search") as search_span:
            distances, indices = faiss_index.search(query_embedding_np, k)
            search_span.set_attribute("faiss.num_results", k)
        
        retrieved_chunks = [docs_chunks[i].page_content for i in indices[0]]
        
        print("\n--- Retrieved Chunks ---")
        for i, chunk in enumerate(retrieved_chunks):
            print(f"Chunk {i+1}:\n{chunk}\n")

        # --- 5. Augment and Generate (Mock LLM) ---
        with tracer.start_as_current_span("generate_response") as gen_span:
            augmented_prompt = (
                "Based on the following context, answer the question.\n\n"
                f"Context:\n{''.join(retrieved_chunks)}\n\n"
                f"Question: {query}"
            )
            
            gen_span.set_attribute("generation.input", augmented_prompt)
            print("--- Augmented Prompt ---")
            print(augmented_prompt)

            # --- Mock LLM Response ---
            # Replace this with an actual LLM call for a complete trace.
            print("\n--- Generating Response (Mock) ---")
            mock_response = "This would be the LLM's final answer, grounded in the retrieved context."
            gen_span.set_attribute("generation.output", mock_response)
        
    return "This would be the LLM's final answer, grounded in the retrieved context."

# --- Main Query Loop ---
if __name__ == "__main__":
    while True:
        user_query = input("\nEnter your question (or 'quit' to exit): ")
        if user_query.lower() == 'quit':
            break
        
        response = retrieve_and_generate(user_query)
        print(f"\nFinal Response: {response}")

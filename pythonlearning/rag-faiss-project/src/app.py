import pickle
import faiss
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
import numpy as np

# --- Configuration ---
MODEL_NAME = "all-MiniLM-L6-v2"
INDEX_SAVE_PATH = "models/faiss_index.pkl"
CHUNKS_SAVE_PATH = "models/docs_chunks.pkl"

# --- 1. Load Pre-trained Index and Chunks ---
print("Loading Faiss index and document chunks...")
with open(INDEX_SAVE_PATH, "rb") as f:
    faiss_index = pickle.load(f)

with open(CHUNKS_SAVE_PATH, "rb") as f:
    docs_chunks = pickle.load(f)

# --- 2. Initialize the Embedding Model ---
embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)

def retrieve_and_generate(query, k=3):
    """
    Performs the RAG process: retrieves relevant docs and generates a response.
    """
    # --- 3. Embed the Query ---
    query_embedding = embeddings.embed_query(query)
    query_embedding_np = np.array([query_embedding]).astype("float32")

    # --- 4. Similarity Search (Faiss) ---
    distances, indices = faiss_index.search(query_embedding_np, k)
    
    retrieved_chunks = [docs_chunks[i].page_content for i in indices[0]]
    
    print("\n--- Retrieved Chunks ---")
    for i, chunk in enumerate(retrieved_chunks):
        print(f"Chunk {i+1}:\n{chunk}\n")

    # --- 5. Augment and Generate (Mock LLM) ---
    # In a real-world scenario, you'd call an LLM API here (e.g., OpenAI, HuggingFace)
    # The prompt would be crafted with the retrieved context.
    
    augmented_prompt = (
        "Based on the following context, answer the question.\n\n"
        f"Context:\n{''.join(retrieved_chunks)}\n\n"
        f"Question: {query}"
    )
    
    print("--- Augmented Prompt ---")
    print(augmented_prompt)

    # --- Mock LLM Response ---
    # For this example, we'll just return the augmented prompt.
    # Replace this with an actual LLM call.
    print("\n--- Generating Response (Mock) ---")
    return "This would be the LLM's final answer, grounded in the retrieved context."

# --- Main Query Loop ---
if __name__ == "__main__":
    while True:
        user_query = input("\nEnter your question (or 'quit' to exit): ")
        if user_query.lower() == 'quit':
            break
        
        response = retrieve_and_generate(user_query)
        print(f"\nFinal Response: {response}")
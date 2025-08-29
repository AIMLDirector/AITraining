import os
import pickle
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
import faiss
import numpy as np

# --- Configuration ---
DATA_DIR = "/Users/premkumargontrand/AITraining/pythonlearning/rag-faiss-project/data/"
MODEL_NAME = "all-MiniLM-L6-v2"
INDEX_SAVE_PATH = "models/faiss_index.pkl"
CHUNKS_SAVE_PATH = "models/docs_chunks.pkl"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# --- 1. Load Data ---all_texts = []
all_texts = []
for filename in os.listdir(DATA_DIR):
    if filename.endswith(".txt"):
        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            all_texts.append(f.read())

print(f"Loaded {len(all_texts)} documents from the data directory.")

# --- 2. Text Splitting (Chunking) ---
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    length_function=len,
    add_start_index=True,
)
docs_chunks = text_splitter.create_documents(all_texts)
print(f"Total number of chunks: {len(docs_chunks)}")

# --- 3. Embedding Generation ---
embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
doc_embeddings = embeddings.embed_documents([chunk.page_content for chunk in docs_chunks])
print(f"Embedding dimension: {len(doc_embeddings[0])}")

# --- 4. Faiss Index Creation ---
# Convert embeddings to a NumPy array for Faiss
doc_embeddings_np = np.array(doc_embeddings).astype("float32")
dimension = doc_embeddings_np.shape[1]

# Create a Faiss Index
# IndexFlatL2 is a simple L2 (Euclidean distance) index.
faiss_index = faiss.IndexFlatL2(dimension)
faiss_index.add(doc_embeddings_np)
print(f"Faiss index has {faiss_index.ntotal} vectors.")

# --- 5. Save the Index and Chunks ---
if not os.path.exists("models"):
    os.makedirs("models")

with open(INDEX_SAVE_PATH, "wb") as f:
    pickle.dump(faiss_index, f)

with open(CHUNKS_SAVE_PATH, "wb") as f:
    pickle.dump(docs_chunks, f)

print("Faiss index and document chunks saved successfully.")
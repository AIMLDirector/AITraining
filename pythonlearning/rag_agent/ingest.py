# ingest.py
from dotenv import load_dotenv
load_dotenv()

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from tqdm import tqdm

DATA_DIR = "data"
CHROMA_DIR = "./chroma_db"

def load_documents():
    docs = []
    for file in os.listdir(DATA_DIR):
        if file.endswith(".pdf"):
            path = os.path.join(DATA_DIR, file)
            loader = PyPDFLoader(path)
            docs.extend(loader.load())
    return docs

def main():
    docs = load_documents()
    print(f"Loaded {len(docs)} pages")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = []
    for d in tqdm(docs, desc="splitting"):
        chunks.extend(splitter.split_documents([d]))

    print(f"Created {len(chunks)} chunks")

    embeddings = OpenAIEmbeddings()
    db_name = CHROMA_DIR

    vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=db_name)
    print(f"Vectorstore created with {vectorstore._collection.count()} documents")
    collection = vectorstore._collection
    sample_embedding = collection.get(limit=1, include=["embeddings"])["embeddings"][0]
    dimensions = len(sample_embedding)
    print(f"The vectors have {dimensions:,} dimensions")

if __name__ == "__main__":
    main()

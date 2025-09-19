import os
from huggingface_hub import login
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector
from dotenv import load_dotenv

load_dotenv()

login(token=os.environ.get("HF_TOKEN"))

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


vector_store = PGVector(
    embeddings=embeddings,
    collection_name="my_docs",
    connection="postgresql://neondb_owner:npg_k1mMwZBz7rqa@ep-dawn-unit-adoommit-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require",
)

print("Vector store initialized:", vector_store)


from huggingface_hub import login
import os
from dotenv import load_dotenv
load_dotenv()
#print(os.environ.get("HF_TOKEN"))
#login()
login(token=os.environ.get("HF_TOKEN"))

from langchain_huggingface import HuggingFaceEmbeddings

HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


from langchain_community.document_loaders import DirectoryLoader, UnstructuredFileLoader, PyPDFLoader, TextLoader, CSVLoader
import os

if os.path.exists("./my_data_directory"):
    print("Directory exists we can load the data")
else:
    exit(1)


# Example: Load PDF, TXT, and CSV files
loader = DirectoryLoader( 
    "./my_data_directory",
    glob="**/*.@(pdf|txt|csv)",  # Matches PDF, TXT, and CSV files
    loader_cls=UnstructuredFileLoader, # UnstructuredFileLoader can handle many formats
    use_multithreading=True # Optional: for faster loading
)
documents = loader.load()  # ( all the document into one document )

print(documents)



from langchain_community.document_loaders import DirectoryLoader, CSVLoader, PyPDFLoader, TextLoader, WebBaseLoader

all_documents = []

# Load CSV files
csv_loader = DirectoryLoader("./my_data_directory", glob="**/*.csv", loader_cls=CSVLoader)
all_documents.extend(csv_loader.load())

# Load PDF files
pdf_loader = DirectoryLoader("./my_data_directory", glob="**/*.pdf", loader_cls=PyPDFLoader)
all_documents.extend(pdf_loader.load())

# Load TXT files
txt_loader = DirectoryLoader("./my_data_directory", glob="**/*.txt", loader_cls=TextLoader)
all_documents.extend(txt_loader.load())

web_loader = WebBaseLoader("https://www.example.com/your-article")  # proxy or firewall  will block your access 
web_documents = web_loader.load()
documents.extend(web_documents)

# Now 'all_documents' contains documents from all specified formats

import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader, UnstructuredHTMLLoader, JSONLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_chunk_directory(directory_path, chunk_size=1000, chunk_overlap=200):
    all_documents = []
    
    for filename in os.listdir(directory_path):
        filepath = os.path.join(directory_path, filename)
        
        if filename.endswith(".txt"):
            loader = TextLoader(filepath)
        elif filename.endswith(".pdf"):
            loader = PyPDFLoader(filepath)
        elif filename.endswith(".html"):
            loader = UnstructuredHTMLLoader(filepath) # Or BSHTMLLoader
        elif filename.endswith(".json"):
            # You might need to define a jq_schema for JSONLoader
            loader = JSONLoader(filepath, jq_schema=".content") 
        else:
            print(f"Skipping unsupported file type: {filename}")
            continue
            
        all_documents.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )
    
    chunks = text_splitter.split_documents(all_documents)
    return chunks

# Example usage:
# directory = "./my_data_directory"
# document_chunks = load_and_chunk_directory(directory)
# for chunk in document_chunks:
#     print(chunk.page_content)

#################################################################
from langchain_community.document_loaders import WebBaseLoader

web_loader = WebBaseLoader("https://www.example.com/your-article")
web_documents = web_loader.load()
documents.extend(web_documents)


#https://python.langchain.com/docs/concepts/document_loaders/
#https://python.langchain.com/docs/concepts/text_splitters/#text-structured-based

# https://python.langchain.com/docs/how_to/semantic-chunker/
#https://python.langchain.com/docs/concepts/vectorstores/
import chromadb
from chromadb.utils import embedding_functions

client = chromadb.Client()
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

def get_collection(collection_name: str):
    return client.get_or_create_collection(collection_name, embedding_function=ef)

def add_chunks(collection_name: str, chunks: list):
    collection = get_collection(collection_name)
    collection.add(documents=chunks, ids= [str(i) for i in range(len(chunks))])
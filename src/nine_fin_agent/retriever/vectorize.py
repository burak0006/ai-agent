from langchain_core.tools import tool
from langchain_community.vectorstores import Qdrant
from langchain.docstore.document import Document
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from typing import Tuple, List
from dotenv import load_dotenv
import os

load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION")
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_PORT = os.getenv("QDRANT_PORT")
EMBEDDING = os.getenv("EMBEDDING")

# initialize embeddings + client + vectorstore
embeddings = OpenAIEmbeddings(model=EMBEDDING)
client = QdrantClient(url=QDRANT_HOST, port=QDRANT_PORT)
vector_store = Qdrant(
    client=client,
    collection_name=QDRANT_COLLECTION,
    embeddings=embeddings,
    )

def _retrieve_raw(query: str, k: int = 5) -> Tuple[str, List[Document]]:
    """
    Raw Python function used by evaluation & unit tests.
    Returns (serialized_text, retrieved_docs).
    """
    retrieved_docs = vector_store.similarity_search(query, k=k)
    serialized = "\n\n".join(
        f"Source: {doc.metadata}\nContent: {doc.page_content}"
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs

@tool(response_format="content_and_artifact")
def retrieve(query: str):
    """Retrieve information related to a query from Qdrant."""
    retrieved_docs = vector_store.similarity_search(query, k=5)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs


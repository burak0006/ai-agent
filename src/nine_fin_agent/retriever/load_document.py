from dotenv import load_dotenv
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant

from pathlib import Path
import logging
import json
import os

# --- Logging setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# --- Config ---
load_dotenv()

ROOT_DIR = Path(__file__).resolve().parents[3]
DOC_PATH = ROOT_DIR / "data" / "synthesized.json"

QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION")
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_PORT = os.getenv("QDRANT_PORT")
EMBEDDING = os.getenv("EMBEDDING")


def load_document(doc_path: str) -> list[Document]:
    """Load synthesized documents from JSON file (with text + metadata)."""
    logger.info(f"Loading documents from {doc_path}")
    with open(doc_path, "r") as f:
        items = json.load(f)

    docs = [
        Document(page_content=item["text"], metadata=item.get("metadata", {}))
        for item in items
    ]

    logger.info(f"Loaded {len(docs)} documents with metadata")
    return docs


def load_and_index(docs: list[Document]):
    """Split documents into chunks and index into Qdrant."""
    logger.info("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=50)
    splits = text_splitter.split_documents(docs)
    logger.info(f"Created {len(splits)} chunks from {len(docs)} docs")

    logger.info(f"Creating embeddings with model={EMBEDDING}")
    embeddings = OpenAIEmbeddings(model=EMBEDDING)

    logger.info(
        f"Indexing into Qdrant (collection={QDRANT_COLLECTION}, host={QDRANT_HOST}, port={QDRANT_PORT})"
    )
    vectorstore = Qdrant.from_documents(
        documents=splits,
        embedding=embeddings,
        collection_name=QDRANT_COLLECTION,
        url=QDRANT_HOST,
        port=QDRANT_PORT,
        force_recreate=True,
    )

    logger.info(
        f"Indexed {len(splits)} chunks into Qdrant collection '{QDRANT_COLLECTION}'"
    )
    return vectorstore

# REDUNDANT CODES FOR TESTING

#if __name__ == "__main__":
#    client = QdrantClient(url=QDRANT_HOST, port=QDRANT_PORT)
#    collection = "financial_data"
#    client.delete_collection(collection_name=collection)
#     docs = load_document(DOC_PATH)
#     load_and_index(docs)

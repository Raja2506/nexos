import chromadb
from app.config import SETTINGS

# Persistent client - saves data to disk, survives restarts
chroma_client = chromadb.PersistentClient(path=SETTINGS["CHROMA_PERSIST_DIR"])

# One collection to hold all agent memories (like a "table" in SQL terms)
collection = chroma_client.get_or_create_collection(name="nexos_memory")


def add_memory(memory_id: str, text: str, metadata: dict) -> None:
    """Store a piece of text with its meaning, so it can be found later by similarity."""
    collection.add(
        ids=[memory_id],
        documents=[text],
        metadatas=[metadata],
    )


def search_memory(query_text: str, n_results: int = 3) -> dict:
    """Find the most semantically similar stored memories to the query."""
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
    )
    return results


def delete_memory(memory_id: str) -> None:
    """Remove a specific memory by its ID."""
    collection.delete(ids=[memory_id])
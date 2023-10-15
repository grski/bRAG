from qdrant_client import QdrantClient

from settings import settings


def test_populate_vector_db(client: QdrantClient):
    # Prepare your documents, metadata, and IDs
    docs = (
        "LoremIpsum sit dolorem",
        "Completely random phrase",
        "Another random phrase",
        "pdf-BRAG is awesome.",
    )
    metadata = (
        {"source": "Olaf"},
        {"source": "grski"},
        {"source": "Olaf"},
        {"source": "grski"},
    )
    ids = [42, 2, 3, 5]

    # Use the new add method
    client.add(
        collection_name=settings.QDRANT_COLLECTION_NAME,
        documents=docs,
        metadata=metadata,
        ids=ids,
    )

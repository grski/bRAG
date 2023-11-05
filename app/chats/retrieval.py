from qdrant_client import QdrantClient

from app.chats.exceptions import RetrievalNoDocumentsFoundException
from app.chats.ingest import test_populate_vector_db
from app.chats.models import BaseMessage
from app.core.logs import logger
from settings import settings

client = QdrantClient(settings.QDRANT_HOST, port=settings.QDRANT_PORT)

# ONLY FOR TEST PURPOSE
test_populate_vector_db(client=client)


def process_retrieval(message: BaseMessage) -> BaseMessage:
    """Search for a given query using vector similarity search. If no documents are found we raise an exception.
    If we do find documents we take the top 3 and put them into the context.
    """
    search_result = search(query=message.message)
    resulting_query: str = (
        f"Answer based only on the context, nothing else. \n"
        f"QUERY:\n{message.message}\n"
        f"CONTEXT:\n{search_result}"
    )
    logger.info(f"Resulting Query: {resulting_query}")
    return BaseMessage(message=resulting_query, model=message.model)


def search(query: str) -> str:
    """Function takes our query string, transforms the string into vectors and then searches for the most similar
    documents, returning the top 3. If no documents are found we raise an exception - as the user is asking
    about something not in the context of our documents.
    """
    search_result = client.query(
        collection_name=settings.QDRANT_COLLECTION_NAME, limit=3, query_text=query
    )
    print(search_result)
    if not search_result:
        raise RetrievalNoDocumentsFoundException
    return "\n".join(result.document for result in search_result)

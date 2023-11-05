from faststream import FastStream
from faststream.nats import NatsBroker
from qdrant_client import QdrantClient

from app.data.models import TextIngestion
from settings import settings

broker = NatsBroker(settings.NATS_URI)
app = FastStream(broker)

qdrant_client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)


@broker.subscriber(settings.NATS_SUBJECT)
async def process_ingestion(text_ingestion: TextIngestion) -> bool:
    qdrant_client.add(collection_name=settings.QDRANT_COLLECTION_NAME, documents=[text_ingestion.text])
    return True

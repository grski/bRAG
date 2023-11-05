from faststream.nats import NatsBroker

from app.data.models import TextIngestion
from settings import settings


async def publish_review(broker: NatsBroker, ingested_text: TextIngestion):
    await broker.publish(
        ingested_text,
        subject=settings.NATS_SUBJECT,
    )

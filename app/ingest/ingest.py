import fnmatch
import os
import uuid

from faststream.nats import NatsBroker

from app.core.logs import logger
from app.data.models import TextIngestion
from app.ingest.publisher import publish_review
from settings import settings


def find_md_files(directory):
    # List to store found md files
    md_files = []

    # Walk through directory
    for root, _dirs, files in os.walk(directory):
        for filename in fnmatch.filter(files, "*.md"):
            # append full file path to our files list
            md_files.append(os.path.join(root, filename))

    return md_files


async def ingest_markdown():
    run_uuid = uuid.uuid4()
    async with NatsBroker(settings.NATS_URI) as broker:
        md_files = find_md_files("data")
        for md_file in md_files:
            with open(md_file, "r") as f:
                ingested_file = TextIngestion(text=f.read(), run_uuid=run_uuid)
                logger.info(f"Publishing review: {ingested_file.text[:50]}")
                await publish_review(broker=broker, ingested_text=ingested_file)
    return run_uuid

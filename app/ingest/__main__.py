import asyncio

from app.ingest.ingest import ingest_markdown

asyncio.run(ingest_markdown())

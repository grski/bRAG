import asyncio
import json

import async_timeout

from app.chats.constants import ChatRolesEnum
from app.chats.exceptions import (
    OpenAIFailedProcessingException,
    OpenAIStreamTimeoutException,
)
from app.chats.models import Chunk, Message
from app.core.logs import logger
from app.db import messages_queries
from settings import settings


async def stream_generator(subscription):
    """In the future if we are paranoid about performance we can pre-allocate a buffer and use it instead of f-string
    should save a cycle or two in the processor or be a fun exercise but totally not worth the effort or complexity
    currently (in the future too).
    """
    async with async_timeout.timeout(settings.GENERATION_TIMEOUT_SEC):
        try:
            complete_response: str = ""
            async for chunk in subscription:
                # f-string is faster than concatenation so we use it here
                complete_response = f"{complete_response}{Chunk.get_chunk_delta_content(chunk=chunk)}"
                yield format_to_event_stream(post_processing(chunk))
            message: Message = Message(
                model=chunk.model,
                message=complete_response,
                role=ChatRolesEnum.ASSISTANT.value,
            )
            messages_queries.insert(model=message.model, message=message.message, role=message.role)
            logger.info(f"Complete Streamed Message: {message}")
        except asyncio.TimeoutError:
            raise OpenAIStreamTimeoutException


def format_to_event_stream(data: str) -> str:
    """We format the event to a format more in line with the standard SSE format."""
    return f"event: message\ndata: {data}\n\n"


def post_processing(chunk) -> str:
    try:
        logger.info(f"Chunk: {chunk}")
        formatted_chunk = Chunk.from_chunk(chunk=chunk)
        logger.info(f"Formatted Chunk: {formatted_chunk}")
        return json.dumps(formatted_chunk.model_dump())
    except Exception:
        raise OpenAIFailedProcessingException

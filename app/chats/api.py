from fastapi import APIRouter

import openai
from starlette.responses import StreamingResponse

from app.chats.exceptions import OpenAIException
from app.chats.models import BaseMessage, Message
from app.chats.services import OpenAIService
from app.db import messages_queries

router = APIRouter(tags=["Chat Endpoints"])


@router.get("/v1/messages")
async def get_messages() -> list[Message]:
    # a bit messy as we might want to move this to a service
    return [Message(**message) for message in messages_queries.select_all()]


@router.post("/v1/completion")
async def completion_create(input_message: BaseMessage) -> Message:
    try:
        return await OpenAIService.chat_completion_without_streaming(input_message=input_message)
    except openai.OpenAIError:
        raise OpenAIException


@router.post("/v1/completion-stream")
async def completion_stream(input_message: BaseMessage) -> StreamingResponse:
    """Streaming response won't return json but rather a properly formatted string for SSE."""
    try:
        return await OpenAIService.chat_completion_with_streaming(input_message=input_message)
    except openai.OpenAIError:
        raise OpenAIException


@router.post("/v1/qa-create")
async def qa_create(input_message: BaseMessage) -> Message:
    try:
        return await OpenAIService.qa_without_stream(input_message=input_message)
    except openai.OpenAIError:
        raise OpenAIException


@router.post("/v1/qa-stream")
async def qa_stream(input_message: BaseMessage) -> StreamingResponse:
    """Streaming response won't return json but rather a properly formatted string for SSE."""
    try:
        return await OpenAIService.qa_with_stream(input_message=input_message)
    except openai.OpenAIError:
        raise OpenAIException

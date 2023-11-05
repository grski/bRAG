import openai
from openai import ChatCompletion
from starlette.responses import StreamingResponse

from app.chats.constants import NO_DOCUMENTS_FOUND, ChatRolesEnum
from app.chats.exceptions import RetrievalNoDocumentsFoundException
from app.chats.models import BaseMessage, Message
from app.chats.retrieval import process_retrieval
from app.chats.streaming import format_to_event_stream, stream_generator
from app.core.logs import logger
from app.db import messages_queries
from settings import settings


class OpenAIService:
    @classmethod
    async def chat_completion_without_streaming(
        cls, input_message: BaseMessage
    ) -> Message:
        completion: openai.ChatCompletion = await openai.ChatCompletion.acreate(
            model=input_message.model,
            api_key=settings.OPENAI_API_KEY,
            messages=[
                {"role": ChatRolesEnum.USER.value, "content": input_message.message}
            ],
        )
        logger.info(f"Got the following response: {completion}")
        message = Message(
            model=input_message.model,
            message=cls.extract_response_from_completion(completion),
            role=ChatRolesEnum.ASSISTANT.value,
        )
        messages_queries.insert(
            model=message.model, message=message.message, role=message.role
        )
        return message

    @staticmethod
    async def chat_completion_with_streaming(
        input_message: BaseMessage,
    ) -> StreamingResponse:
        subscription: openai.ChatCompletion = await openai.ChatCompletion.acreate(
            model=input_message.model,
            api_key=settings.OPENAI_API_KEY,
            messages=[
                {"role": ChatRolesEnum.USER.value, "content": input_message.message}
            ],
            stream=True,
        )
        return StreamingResponse(
            stream_generator(subscription), media_type="text/event-stream"
        )

    @staticmethod
    def extract_response_from_completion(chat_completion: ChatCompletion) -> str:
        return chat_completion.choices[0]["message"]["content"]

    @classmethod
    async def qa_without_stream(cls, input_message: BaseMessage) -> Message:
        try:
            augmented_message: BaseMessage = process_retrieval(message=input_message)
            return await cls.chat_completion_without_streaming(
                input_message=augmented_message
            )
        except RetrievalNoDocumentsFoundException:
            return Message(
                model=input_message.model,
                message=NO_DOCUMENTS_FOUND,
                role=ChatRolesEnum.ASSISTANT.value,
            )

    @classmethod
    async def qa_with_stream(cls, input_message: BaseMessage) -> StreamingResponse:
        try:
            augmented_message: BaseMessage = process_retrieval(message=input_message)
            return await cls.chat_completion_with_streaming(
                input_message=augmented_message
            )
        except RetrievalNoDocumentsFoundException:
            return StreamingResponse(
                (format_to_event_stream(y) for y in "Not found"),
                media_type="text/event-stream",
            )

from uuid import UUID

import openai
from openai import AsyncOpenAI, OpenAI
from openai.types.chat import ChatCompletion
from starlette.responses import StreamingResponse

from app.chats.constants import NO_DOCUMENTS_FOUND, ChatRolesEnum
from app.chats.exceptions import RetrievalNoDocumentsFoundException
from app.chats.models import Assistant, BaseMessage, Chat, Message
from app.chats.retrieval import process_retrieval
from app.chats.streaming import format_to_event_stream, stream_generator
from app.core.logs import logger
from app.db import assistants_queries, chats_queries, messages_queries
from settings import settings

openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
async_openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


def create_openai_thread(chat_uuid):
    openai_id = openai_client.beta.threads.create().id
    chat = Chat(openai_id=openai_id, uuid=chat_uuid)
    chats_queries.insert_chat(uuid=chat.uuid, openai_thread_id=chat.openai_id)
    return chat


def create_openai_assistant():
    openai_id = openai_client.beta.assistants.create(
        instructions="You are a helpul instruction following assistant.",
        name="Helpful Assistant",
        model="gpt-4",
    ).id
    assistant = Assistant(openai_id=openai_id)
    assistants_queries.insert_assistant(uuid=assistant.uuid, openai_id=assistant.openai_id)
    return assistant


class BetaOpenAIService:
    def __init__(self, chat_uuid: UUID):
        self.assistant: Assistant = self.get_or_init_assistant()
        self.chat: Chat = self.get_or_init_chat(chat_uuid=chat_uuid)

    @staticmethod
    def get_or_init_chat(chat_uuid: UUID) -> Chat:
        if chat := chats_queries.get_chat(uuid=chat_uuid):
            return Chat(uuid=chat["uuid"], openai_id=chat["openai_id"])
        return create_openai_thread(chat_uuid=chat_uuid)

    @staticmethod
    def get_or_init_assistant():
        if assistant := assistants_queries.get_first_assistant():
            return Assistant(uuid=assistant["uuid"], openai_id=assistant["openai_id"])
        return create_openai_assistant()

    async def get_chat(self):
        chat = chats_queries.get_chat(uuid=self.chat.uuid)
        return await async_openai_client.beta.threads.messages.list(
            thread_id=chat["openai_id"]
        )

    async def send_message_to_a_thread(self, input_message: BaseMessage):
        await async_openai_client.beta.threads.messages.create(
            thread_id=self.chat.openai_id,
            role=ChatRolesEnum.USER.value,
            content=input_message.message,
        )
        await async_openai_client.beta.threads.runs.create(
            thread_id=self.chat.openai_id,
            assistant_id=self.assistant.openai_id,
        )
        return self.chat


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
        return chat_completion.choices[0].message.content

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

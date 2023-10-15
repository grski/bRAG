from pydantic import BaseModel, Field

from app.chats.constants import ChatRolesEnum, ModelsEnum
from app.chats.exceptions import OpenAIFailedProcessingException
from app.core.models import TimestampAbstractModel


class BaseMessage(BaseModel):
    """Base pydantic model that we use to interact with the API."""

    model: ModelsEnum = Field(default=ModelsEnum.GPT4.value)
    message: str


class Message(TimestampAbstractModel, BaseMessage):
    id: int = Field(default=None)
    role: ChatRolesEnum


class Chunk(BaseModel):
    id: str
    created: int = Field(default=0)
    model: ModelsEnum = Field(default="gpt-4-0613")
    content: str
    finish_reason: str | None = None

    @classmethod
    def from_chunk(cls, chunk):
        delta_content: str = cls.get_chunk_delta_content(chunk=chunk)
        return cls(
            id=chunk["id"],
            created=chunk["created"],
            model=chunk["model"],
            content=delta_content,
            finish_reason=chunk["choices"][0].get("finish_reason", None),
        )

    @staticmethod
    def get_chunk_delta_content(chunk: dict | str) -> str:
        try:
            match chunk:
                case str(chunk):
                    return chunk
                case dict(chunk):
                    return chunk["choices"][0]["delta"].get("content", "")
        except Exception:
            raise OpenAIFailedProcessingException

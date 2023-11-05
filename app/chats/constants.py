from enum import StrEnum


class FailureReasonsEnum(StrEnum):
    OPENAI_ERROR = "OpenAI call failed"
    STREAM_TIMEOUT = "Stream timed out"
    FAILED_PROCESSING = "Post processing failed"


class ChatRolesEnum(StrEnum):
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"


class ModelsEnum(StrEnum):
    GPT4 = "gpt-4-0613"


NO_DOCUMENTS_FOUND: str = (
    "No documents found in context. Please try again with a different query."
)

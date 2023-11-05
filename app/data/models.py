from uuid import UUID

from pydantic import BaseModel


class TextIngestion(BaseModel):
    text: str
    run_uuid: UUID


class CSVIngestion(BaseModel):
    row: dict

from datetime import datetime

from pydantic import BaseModel, Field


class TimestampAbstractModel(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)

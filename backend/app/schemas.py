from datetime import datetime
from pydantic import BaseModel, ConfigDict


class JournalEntryBase(BaseModel):
    content: str


class JournalEntryCreate(JournalEntryBase):
    pass


class JournalEntryRead(JournalEntryBase):
    id: int
    created_at: datetime
    sentiment: str | None = None
    sentiment_score: float | None = None
    model_config = ConfigDict(from_attributes=True)

from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Text, DateTime, String, Float, JSON
from backend.app.storage.db.base import Base
from pgvector.sqlalchemy import VECTOR


class JournalEntry(Base):
    __tablename__ = "journal_entries"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )

    sentiment: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    sentiment_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    emotions: Mapped[Optional[dict[str, float]]] = mapped_column(JSON, nullable=True)
    embedding: Mapped[Optional[VECTOR]] = mapped_column(VECTOR(384), nullable=True)

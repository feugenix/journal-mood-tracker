from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Text, DateTime, String, Float
from .db import Base


class JournalEntry(Base):
    __tablename__ = "journal_entries"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )

    # Reserved for later NLP features:
    sentiment: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    sentiment_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
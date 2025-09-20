from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select, desc


from backend.app.storage.db.base import get_session
from backend.app import nlp
from backend.app import models, schemas


router = APIRouter(prefix="/entries", tags=["entries"])


@router.get("/", response_model=List[schemas.JournalEntryRead])
async def list_entries(session: AsyncSession = Depends(get_session)):
    stmt = (
        select(models.JournalEntry)
        .order_by(desc(models.JournalEntry.created_at))
        .limit(100)
    )
    res = await session.execute(stmt)
    return res.scalars().all()


@router.post(
    "/", response_model=schemas.JournalEntryRead, status_code=status.HTTP_201_CREATED
)
async def create_entry(
    payload: schemas.JournalEntryCreate, session: AsyncSession = Depends(get_session)
):
    sentiment, score = nlp.analyze_sentiment(payload.content)
    emotions = nlp.analyze_emotions(payload.content)
    embedding = nlp.get_embedding(payload.content)
    keywords = nlp.extract_keywords(payload.content)

    entry = models.JournalEntry(
        content=payload.content,
        sentiment=sentiment,
        sentiment_score=score,
        emotions=emotions,
        embedding=embedding,
        keywords=keywords,
    )
    session.add(entry)

    await session.commit()
    await session.refresh(entry)

    return entry


@router.get("/similar/{entry_id}", response_model=List[schemas.JournalEntryRead])
async def get_similar_entries(
    entry_id: int, session: AsyncSession = Depends(get_session)
):
    entry_embeddings_query = select(models.JournalEntry.embedding).where(
        models.JournalEntry.id == entry_id
    )
    entry_embeddings = (await session.execute(entry_embeddings_query)).scalars().one()

    stmt = (
        select(models.JournalEntry)
        .where(
            and_(
                models.JournalEntry.id != entry_id,
                models.JournalEntry.embedding.is_not(None),
            )
        )
        .order_by(models.JournalEntry.embedding.l2_distance(entry_embeddings).desc())
        .limit(5)
    )

    res = await session.execute(stmt)
    return res.scalars().all()

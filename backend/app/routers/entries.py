from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc


from backend.app.storage.db.base import get_session
from backend.app import models, schemas


router = APIRouter(prefix="/entries", tags=["entries"])

@router.get("/", response_model=List[schemas.JournalEntryRead])
async def list_entries(session: AsyncSession = Depends(get_session)):
    stmt = select(models.JournalEntry).order_by(desc(models.JournalEntry.created_at)).limit(100)
    res = await session.execute(stmt)
    return res.scalars().all()


@router.post("/", response_model=schemas.JournalEntryRead, status_code=status.HTTP_201_CREATED)
async def create_entry(payload: schemas.JournalEntryCreate, session: AsyncSession = Depends(get_session)):
    entry = models.JournalEntry(content=payload.content)
    session.add(entry)
    await session.commit()
    await session.refresh(entry)
    return entry
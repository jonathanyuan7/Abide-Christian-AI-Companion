from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_async_db
from app.models.entry import Entry, EntryType
from app.models.bookmark import Bookmark
from app.models.user import User
from typing import List, Optional
from datetime import datetime

router = APIRouter()

@router.get("/entries")
async def get_user_entries(
    user_id: int,
    entry_type: Optional[EntryType] = None,
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Get user's entries (feelings and devotions)
    """
    try:
        query = select(Entry).where(Entry.user_id == user_id)
        
        if entry_type:
            query = query.where(Entry.type == entry_type)
        
        query = query.order_by(Entry.created_at.desc()).offset(offset).limit(limit)
        
        result = await db.execute(query)
        entries = result.scalars().all()
        
        return {
            "entries": [
                {
                    "id": entry.id,
                    "type": entry.type,
                    "topic": entry.topic,
                    "input_text": entry.input_text,
                    "response": entry.response_json,
                    "created_at": entry.created_at
                }
                for entry in entries
            ],
            "total": len(entries)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving entries: {str(e)}")

@router.get("/bookmarks")
async def get_user_bookmarks(
    user_id: int,
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Get user's bookmarked entries
    """
    try:
        query = select(Bookmark, Entry).join(Entry).where(Bookmark.user_id == user_id)
        query = query.order_by(Bookmark.created_at.desc()).offset(offset).limit(limit)
        
        result = await db.execute(query)
        bookmarks = result.all()
        
        return {
            "bookmarks": [
                {
                    "id": bookmark.id,
                    "entry": {
                        "id": entry.id,
                        "type": entry.type,
                        "topic": entry.topic,
                        "response": entry.response_json,
                        "created_at": entry.created_at
                    },
                    "bookmarked_at": bookmark.created_at
                }
                for bookmark, entry in bookmarks
            ],
            "total": len(bookmarks)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving bookmarks: {str(e)}")

@router.post("/bookmark")
async def bookmark_entry(
    user_id: int,
    entry_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Bookmark an entry
    """
    try:
        # Check if entry exists
        entry_result = await db.execute(select(Entry).where(Entry.id == entry_id))
        entry = entry_result.scalar_one_or_none()
        
        if not entry:
            raise HTTPException(status_code=404, detail="Entry not found")
        
        # Check if already bookmarked
        existing_bookmark = await db.execute(
            select(Bookmark).where(
                Bookmark.user_id == user_id,
                Bookmark.entry_id == entry_id
            )
        )
        
        if existing_bookmark.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Entry already bookmarked")
        
        # Create bookmark
        bookmark = Bookmark(user_id=user_id, entry_id=entry_id)
        db.add(bookmark)
        await db.commit()
        
        return {"message": "Entry bookmarked successfully", "bookmark_id": bookmark.id}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error bookmarking entry: {str(e)}")

@router.delete("/bookmark/{bookmark_id}")
async def remove_bookmark(
    bookmark_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Remove a bookmark
    """
    try:
        # Find and delete bookmark
        bookmark_result = await db.execute(
            select(Bookmark).where(
                Bookmark.id == bookmark_id,
                Bookmark.user_id == user_id
            )
        )
        bookmark = bookmark_result.scalar_one_or_none()
        
        if not bookmark:
            raise HTTPException(status_code=404, detail="Bookmark not found")
        
        await db.delete(bookmark)
        await db.commit()
        
        return {"message": "Bookmark removed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error removing bookmark: {str(e)}")

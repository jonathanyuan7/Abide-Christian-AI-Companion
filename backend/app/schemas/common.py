from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Verse(BaseModel):
    """Bible verse schema"""
    reference: str
    text: str
    translation: str

class Video(BaseModel):
    """YouTube video schema"""
    videoId: str
    title: str
    channelTitle: str
    thumbnailUrl: str
    duration: Optional[int] = None
    description: Optional[str] = None

class User(BaseModel):
    """User schema"""
    id: Optional[int] = None
    email: Optional[str] = None
    supabase_id: Optional[str] = None
    created_at: Optional[datetime] = None
    is_active: bool = True

    class Config:
        from_attributes = True

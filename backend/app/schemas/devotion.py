from pydantic import BaseModel
from typing import List, Optional
from .common import Verse, Video

class DevotionPlan(BaseModel):
    """Devotion plan schema"""
    opening_prayer: str
    scriptures: List[Verse]
    reflection: str
    action_steps: List[str]
    closing_prayer: str

class DevotionRequest(BaseModel):
    """Request schema for devotion generation"""
    theme: Optional[str] = None
    text: Optional[str] = None
    user_id: Optional[int] = None

class DevotionResponse(BaseModel):
    """Response schema for devotion response"""
    plan: DevotionPlan
    video: Video
    theme: str

from pydantic import BaseModel
from typing import List, Optional
from .common import Verse

class FeelingRequest(BaseModel):
    """Request schema for feeling input"""
    text: str
    user_id: Optional[int] = None

class FeelingResponse(BaseModel):
    """Response schema for feeling response"""
    verses: List[Verse]
    reflection: str
    prayer: str
    topic: str
    crisis_detected: Optional[bool] = False
    message: Optional[str] = None
    supportive_verses: Optional[List[Verse]] = None
    resources: Optional[List[str]] = None

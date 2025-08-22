from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_db
from app.schemas.devotion import DevotionRequest, DevotionResponse
from app.services.ai import ResponseGenerator
from app.models.entry import Entry, EntryType
import json

router = APIRouter()

@router.post("/", response_model=DevotionResponse)
async def generate_devotion(
    request: DevotionRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Generate a 10-minute devotion plan with scripture, reflection, and YouTube video
    """
    try:
        response_generator = ResponseGenerator()
        
        # Generate devotion
        devotion = await response_generator.generate_devotion(
            theme=request.theme,
            feeling_text=request.text,
            user_id=request.user_id
        )
        
        # Save entry to database if user is logged in
        if request.user_id:
            entry = Entry(
                user_id=request.user_id,
                type=EntryType.DEVOTION,
                topic=devotion["theme"],
                input_text=request.text if request.text else None,
                response_json=devotion
            )
            db.add(entry)
            await db.commit()
        
        return DevotionResponse(
            plan=devotion["plan"],
            video=devotion["video"],
            theme=devotion["theme"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating devotion: {str(e)}")

@router.get("/themes")
async def get_available_themes():
    """
    Get list of available devotion themes
    """
    themes = [
        "peace", "hope", "comfort", "strength", "love", 
        "gratitude", "anxiety", "loneliness", "forgiveness"
    ]
    return {"themes": themes}

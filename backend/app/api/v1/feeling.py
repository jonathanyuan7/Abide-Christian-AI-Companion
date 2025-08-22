from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_db
from app.schemas.feeling import FeelingRequest, FeelingResponse
from app.services.ai import ResponseGenerator
from app.core.crisis_detection import CrisisDetector
from app.models.entry import Entry, EntryType
from typing import Optional
import json

router = APIRouter()

@router.post("/", response_model=FeelingResponse)
async def process_feeling(
    request: FeelingRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Process a user's feeling and return relevant Bible verses, reflection, and prayer
    """
    try:
        # Check for crisis indicators first
        crisis_detector = CrisisDetector()
        if crisis_detector.detect_crisis(request.text):
            crisis_response = crisis_detector.get_crisis_response(request.text)
            
            # Convert crisis response to FeelingResponse format
            return FeelingResponse(
                verses=crisis_response["supportive_verses"],
                reflection="",  # No reflection for crisis situations
                prayer=crisis_response["prayer"],
                topic=crisis_response["topic"],
                crisis_detected=True,
                message=crisis_response["message"],
                supportive_verses=crisis_response["supportive_verses"],
                resources=crisis_response["resources"]
            )
        
        # Generate normal response
        response_generator = ResponseGenerator()
        response = await response_generator.generate_feeling_response(
            request.text, 
            request.user_id
        )
        
        # Save entry to database if user is logged in
        if request.user_id:
            entry = Entry(
                user_id=request.user_id,
                type=EntryType.FEEL,
                topic=response["topic"],
                input_text=request.text if request.user_id else None,  # Only save text for logged-in users
                response_json=response
            )
            db.add(entry)
            await db.commit()
        
        return FeelingResponse(
            verses=response["verses"],
            reflection=response["reflection"],
            prayer=response["prayer"],
            topic=response["topic"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing feeling: {str(e)}")

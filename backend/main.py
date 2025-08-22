from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import init_db
from app.api.v1.api import api_router
from app.core.crisis_detection import CrisisDetector
from app.core.logging import setup_logging

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    setup_logging()
    yield
    # Shutdown
    pass

app = FastAPI(
    title="Abide: Christian AI Companion",
    description="A gentle, privacy-respecting Christian app for spiritual guidance",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crisis detection middleware
@app.middleware("http")
async def crisis_detection_middleware(request: Request, call_next):
    if request.method == "POST" and request.url.path in ["/api/v1/feel", "/api/v1/devotion"]:
        # Check for crisis indicators in request body
        body = await request.body()
        if body:
            crisis_detector = CrisisDetector()
            if crisis_detector.detect_crisis(body.decode()):
                return JSONResponse(
                    status_code=200,
                    content={
                        "crisis_detected": True,
                        "message": "If you're in immediate danger, contact local emergency services. In the U.S., call or text 988 (Suicide & Crisis Lifeline).",
                        "supportive_verses": [
                            {
                                "reference": "Psalm 34:18",
                                "text": "The LORD is nigh unto them that are of a broken heart; and saveth such as be of a contrite spirit.",
                                "translation": "KJV"
                            }
                        ],
                        "prayer": "Lord, please be with this person in their time of need. Surround them with Your love and protection, and guide them to the help they need. Amen.",
                        "topic": "crisis_support"
                    }
                )
    
    response = await call_next(request)
    return response

# Include API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Welcome to Abide: Christian AI Companion",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "abide-backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

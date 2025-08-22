from fastapi import APIRouter
from .feeling import router as feeling_router
from .devotion import router as devotion_router
from .history import router as history_router

api_router = APIRouter()

api_router.include_router(feeling_router, prefix="/feel", tags=["feeling"])
api_router.include_router(devotion_router, prefix="/devotion", tags=["devotion"])
api_router.include_router(history_router, prefix="/history", tags=["history"])

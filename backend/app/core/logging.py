import logging
import sys
from app.core.config import settings

def setup_logging():
    """Setup logging configuration"""
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO if settings.ENVIRONMENT == "production" else logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )
    
    # Set specific logger levels
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    
    # Create logger for the app
    logger = logging.getLogger("abide")
    logger.setLevel(logging.INFO)
    
    return logger

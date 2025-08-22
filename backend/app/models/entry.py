from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

class EntryType(str, enum.Enum):
    FEEL = "feel"
    DEVOTION = "devotion"

class Entry(Base):
    __tablename__ = "entries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Nullable for guest users
    type = Column(Enum(EntryType), nullable=False)
    topic = Column(String, nullable=False)
    input_text = Column(Text, nullable=True)  # Nullable for privacy
    response_json = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="entries")
    bookmarks = relationship("Bookmark", back_populates="entry")
    
    def __repr__(self):
        return f"<Entry(id={self.id}, type='{self.type}', topic='{self.topic}')>"

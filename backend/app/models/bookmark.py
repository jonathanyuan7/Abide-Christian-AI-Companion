from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Bookmark(Base):
    __tablename__ = "bookmarks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    entry_id = Column(Integer, ForeignKey("entries.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="bookmarks")
    entry = relationship("Entry", back_populates="bookmarks")
    
    def __repr__(self):
        return f"<Bookmark(id={self.id}, user_id={self.user_id}, entry_id={self.entry_id})>"

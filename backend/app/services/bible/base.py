from abc import ABC, abstractmethod
from typing import List, Dict, Optional

class BibleProvider(ABC):
    """Base class for Bible content providers"""
    
    @abstractmethod
    async def get_verses(self, references: List[str], translation: str = "KJV") -> List[Dict]:
        """
        Get Bible verses by reference
        
        Args:
            references: List of Bible references (e.g., ["John 3:16", "Psalm 23:1"])
            translation: Bible translation to use
            
        Returns:
            List of verse dictionaries with reference, text, and translation
        """
        pass
    
    @abstractmethod
    async def search_verses(self, query: str, translation: str = "KJV", limit: int = 5) -> List[Dict]:
        """
        Search for Bible verses by keyword or phrase
        
        Args:
            query: Search query
            translation: Bible translation to use
            limit: Maximum number of results
            
        Returns:
            List of matching verse dictionaries
        """
        pass
    
    @abstractmethod
    async def get_random_verses(self, topic: str, translation: str = "KJV", count: int = 2) -> List[Dict]:
        """
        Get random verses related to a topic
        
        Args:
            topic: Topic or theme (e.g., "peace", "hope", "comfort")
            translation: Bible translation to use
            count: Number of verses to return
            
        Returns:
            List of verse dictionaries
        """
        pass
    
    @abstractmethod
    def get_supported_translations(self) -> List[str]:
        """Get list of supported Bible translations"""
        pass
    
    @abstractmethod
    def is_translation_licensed(self, translation: str) -> bool:
        """Check if a translation is properly licensed for use"""
        pass

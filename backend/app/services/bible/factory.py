from typing import Optional
from app.core.config import settings
from app.services.bible.base import BibleProvider
from app.services.bible.public_domain import PublicDomainProvider

class BibleProviderFactory:
    """Factory for creating Bible providers based on configuration"""
    
    @staticmethod
    def create_provider(provider_type: Optional[str] = None) -> BibleProvider:
        """
        Create a Bible provider instance
        
        Args:
            provider_type: Type of provider to create (defaults to config setting)
            
        Returns:
            BibleProvider instance
        """
        if provider_type is None:
            provider_type = settings.BIBLE_PROVIDER
        
        if provider_type == "public_domain":
            return PublicDomainProvider()
        elif provider_type == "esv":
            # TODO: Implement ESV provider when licensed
            raise NotImplementedError("ESV provider not yet implemented - requires licensing")
        elif provider_type == "niv":
            # TODO: Implement NIV provider when licensed
            raise NotImplementedError("NIV provider not yet implemented - requires licensing")
        else:
            # Default to public domain
            return PublicDomainProvider()
    
    @staticmethod
    def get_available_providers() -> list:
        """Get list of available Bible providers"""
        return ["public_domain"]  # Only public domain is available in MVP
    
    @staticmethod
    def get_provider_info(provider_type: str) -> dict:
        """Get information about a specific provider"""
        providers_info = {
            "public_domain": {
                "name": "Public Domain",
                "description": "Free to use Bible translations (KJV, WEB)",
                "translations": ["KJV", "WEB"],
                "licensed": True,
                "cost": "Free"
            },
            "esv": {
                "name": "English Standard Version",
                "description": "ESV Bible translation (requires licensing)",
                "translations": ["ESV"],
                "licensed": False,
                "cost": "Licensing required"
            },
            "niv": {
                "name": "New International Version",
                "description": "NIV Bible translation (requires licensing)",
                "translations": ["NIV"],
                "licensed": False,
                "cost": "Licensing required"
            }
        }
        
        return providers_info.get(provider_type, {})

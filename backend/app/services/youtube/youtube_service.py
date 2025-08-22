import httpx
from typing import List, Dict, Optional
from app.core.config import settings
from app.core.database import redis_client
import json

class YouTubeService:
    """Service for finding relevant YouTube content"""
    
    def __init__(self):
        self.api_key = settings.YOUTUBE_API_KEY
        self.base_url = "https://www.googleapis.com/youtube/v3"
        self.cache_ttl = 3600  # 1 hour cache
    
    async def search_christian_content(self, theme: str, max_duration: int = 600) -> Optional[Dict]:
        """
        Search for Christian YouTube content related to a theme
        
        Args:
            theme: Theme or topic to search for
            max_duration: Maximum video duration in seconds
            
        Returns:
            Video information or None if no results
        """
        if not self.api_key:
            # Return fallback content if no API key
            return self._get_fallback_content(theme)
        
        # Check cache first
        cache_key = f"youtube_search:{theme}:{max_duration}"
        cached_result = redis_client.get(cache_key)
        if cached_result:
            return json.loads(cached_result)
        
        try:
            # Build search query
            search_query = f"Christian {theme} worship devotional"
            
            # Search parameters
            params = {
                "part": "snippet",
                "q": search_query,
                "type": "video",
                "videoDuration": "medium",  # 4-20 minutes
                "safeSearch": settings.YOUTUBE_SAFE_SEARCH,
                "relevanceLanguage": "en",
                "maxResults": 10,
                "key": self.api_key
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/search", params=params)
                response.raise_for_status()
                
                search_results = response.json()
                
                if not search_results.get("items"):
                    return self._get_fallback_content(theme)
                
                # Get video details including duration
                video_ids = [item["id"]["videoId"] for item in search_results["items"][:5]]
                video_details = await self._get_video_details(video_ids)
                
                # Filter by duration and find best match
                suitable_videos = []
                for video in video_details:
                    duration = self._parse_duration(video.get("contentDetails", {}).get("duration", ""))
                    if duration <= max_duration and duration >= settings.YOUTUBE_MIN_DURATION:
                        suitable_videos.append({
                            "videoId": video["id"],
                            "title": video["snippet"]["title"],
                            "channelTitle": video["snippet"]["channelTitle"],
                            "thumbnailUrl": video["snippet"]["thumbnails"]["medium"]["url"],
                            "duration": duration,
                            "description": video["snippet"]["description"][:200] + "..." if len(video["snippet"]["description"]) > 200 else video["snippet"]["description"]
                        })
                
                if not suitable_videos:
                    return self._get_fallback_content(theme)
                
                # Select best video (prefer shorter ones for devotions)
                best_video = min(suitable_videos, key=lambda x: abs(x["duration"] - 300))  # Prefer ~5 min
                
                # Cache the result
                redis_client.setex(cache_key, self.cache_ttl, json.dumps(best_video))
                
                return best_video
                
        except Exception as e:
            # Log error and return fallback
            print(f"YouTube API error: {e}")
            return self._get_fallback_content(theme)
    
    async def _get_video_details(self, video_ids: List[str]) -> List[Dict]:
        """Get detailed information about videos"""
        if not video_ids:
            return []
        
        params = {
            "part": "snippet,contentDetails",
            "id": ",".join(video_ids),
            "key": self.api_key
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/videos", params=params)
            response.raise_for_status()
            
            return response.json().get("items", [])
    
    def _parse_duration(self, duration: str) -> int:
        """Parse ISO 8601 duration string to seconds"""
        import re
        
        # Parse PT4M13S format
        match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
        if not match:
            return 0
        
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)
        
        return hours * 3600 + minutes * 60 + seconds
    
    def _get_fallback_content(self, theme: str) -> Dict:
        """Return fallback content when YouTube API is unavailable"""
        fallback_videos = {
            "peace": {
                "videoId": "dQw4w9WgXcQ",  # Placeholder
                "title": "Peaceful Christian Worship",
                "channelTitle": "Christian Music",
                "thumbnailUrl": "https://via.placeholder.com/320x180/4F46E5/FFFFFF?text=Peace+Worship",
                "duration": 300,
                "description": "A peaceful worship song to help you find God's peace."
            },
            "hope": {
                "videoId": "dQw4w9WgXcQ",  # Placeholder
                "title": "Hope in Christ",
                "channelTitle": "Christian Devotionals",
                "thumbnailUrl": "https://via.placeholder.com/320x180/059669/FFFFFF?text=Hope+Devotional",
                "duration": 300,
                "description": "A devotional message about finding hope in Christ."
            },
            "comfort": {
                "videoId": "dQw4w9WgXcQ",  # Placeholder
                "title": "Comfort from Scripture",
                "channelTitle": "Bible Study",
                "thumbnailUrl": "https://via.placeholder.com/320x180/DC2626/FFFFFF?text=Comfort+Scripture",
                "duration": 300,
                "description": "Scripture readings to bring comfort in difficult times."
            }
        }
        
        # Return theme-specific fallback or default
        return fallback_videos.get(theme.lower(), fallback_videos["peace"])
    
    async def get_worship_songs(self, theme: str) -> List[Dict]:
        """Get worship songs related to a theme"""
        # This could be expanded to search specifically for worship music
        return [await self.search_christian_content(theme, max_duration=600)]
    
    async def get_devotional_content(self, theme: str) -> List[Dict]:
        """Get devotional content related to a theme"""
        # This could be expanded to search specifically for devotional content
        return [await self.search_christian_content(theme, max_duration=600)]

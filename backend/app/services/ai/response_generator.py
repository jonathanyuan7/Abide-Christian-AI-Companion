import json
import random
from typing import List, Dict, Optional
from app.services.bible import BibleProviderFactory
from app.services.youtube import YouTubeService
from app.core.config import settings

class ResponseGenerator:
    """Generates AI responses for feelings and devotions"""
    
    def __init__(self):
        self.bible_provider = BibleProviderFactory.create_provider()
        self.youtube_service = YouTubeService()
        
        # Pre-defined response templates for deterministic output
        self.feeling_templates = {
            "peace": {
                "reflection": "In moments when you're seeking peace, remember that God offers a peace that surpasses all understanding. His peace isn't dependent on circumstances but flows from His presence in your life. When you feel overwhelmed, take a moment to breathe and remember that He is with you, holding you in His loving arms.",
                "prayer": "Lord, please fill this person's heart with Your perfect peace. Help them to rest in Your presence and trust in Your care. Amen."
            },
            "hope": {
                "reflection": "Hope is not just wishful thinking—it's a confident expectation based on God's promises. Even when life feels dark, God's light never goes out. He has plans for your good and a future filled with hope. Hold onto His promises, for they are true and trustworthy.",
                "prayer": "Heavenly Father, please renew this person's hope and remind them of Your faithful promises. Help them to see Your light even in difficult times. Amen."
            },
            "comfort": {
                "reflection": "God is close to the brokenhearted and saves those who are crushed in spirit. He doesn't promise that life will be easy, but He does promise to be with you through every trial. His comfort is real and His love is constant, even when you can't feel it.",
                "prayer": "Lord, please wrap this person in Your loving arms and bring them the comfort only You can provide. Help them to feel Your presence. Amen."
            },
            "strength": {
                "reflection": "God doesn't call you to be strong on your own—He calls you to rely on His strength. When you feel weak, that's when His power is made perfect in you. He gives strength to the weary and increases the power of the weak. Trust in His strength, not your own.",
                "prayer": "Father, please fill this person with Your strength and power. Help them to rely on You and find their strength in You alone. Amen."
            },
            "love": {
                "reflection": "God's love for you is unconditional and never-ending. Nothing can separate you from His love—not your mistakes, not your doubts, not even your feelings. He loved you before you were born and will love you for all eternity. Rest in that love.",
                "prayer": "Lord, please help this person to truly understand and feel Your deep, abiding love. Let them rest in the security of Your love. Amen."
            },
            "gratitude": {
                "reflection": "Gratitude is a powerful practice that shifts our focus from what we lack to what we have. Every good gift comes from God, and when we recognize His blessings, our hearts overflow with thankfulness. Gratitude opens our eyes to see God's goodness all around us.",
                "prayer": "Father, thank You for all Your blessings. Help this person to see Your goodness and respond with a grateful heart. Amen."
            },
            "anxiety": {
                "reflection": "Anxiety often comes from trying to control things that are beyond our control. God invites you to cast all your cares on Him because He cares for you. He holds the future in His hands, and He is working all things for your good. Trust Him with your worries.",
                "prayer": "Lord, please calm this person's anxious heart and help them to trust You with their concerns. Give them Your peace that passes understanding. Amen."
            },
            "loneliness": {
                "reflection": "Even in your loneliest moments, you are never truly alone. God is always with you, and He understands what it feels like to be alone. He promises to never leave you or forsake you. His presence is real, even when you can't feel it.",
                "prayer": "Father, please remind this person that You are always with them. Help them to feel Your loving presence and know they are never alone. Amen."
            }
        }
        
        # Devotion templates
        self.devotion_templates = {
            "peace": {
                "opening_prayer": "Lord, as we begin this time with You, please quiet our hearts and minds. Help us to focus on Your presence and receive Your peace. Amen.",
                "reflection": "Peace is not the absence of trouble, but the presence of God in the midst of trouble. When we focus on God's character and promises rather than our circumstances, we can experience His peace that surpasses all understanding. This peace guards our hearts and minds, protecting us from anxiety and fear.",
                "action_steps": [
                    "Take 5 deep breaths, focusing on God's presence with each breath",
                    "Write down one thing you're worried about and give it to God in prayer"
                ],
                "closing_prayer": "Father, thank You for Your peace that guards our hearts. Help us to carry this peace with us throughout our day. Amen."
            },
            "hope": {
                "opening_prayer": "Heavenly Father, open our hearts to receive Your hope today. Help us to see beyond our current circumstances to Your promises. Amen.",
                "reflection": "Hope is an anchor for our souls, keeping us steady in life's storms. God's hope is not wishful thinking but confident expectation based on His character and promises. When we place our hope in God, we can face any challenge with confidence, knowing He is working for our good.",
                "action_steps": [
                    "Read one of today's verses aloud and reflect on what it reveals about God's character",
                    "Write down one way you can share hope with someone else today"
                ],
                "closing_prayer": "Lord, thank You for the hope we have in You. Help us to share this hope with others. Amen."
            },
            "comfort": {
                "opening_prayer": "God of all comfort, be with us in this time. Wrap us in Your loving arms and bring us the comfort only You can provide. Amen.",
                "reflection": "God comforts us in our affliction so that we can comfort others. His comfort is not just for our benefit but equips us to be His hands and feet to those around us. When we receive God's comfort, we become channels of His love to others who are hurting.",
                "action_steps": [
                    "Reflect on a time when God comforted you and thank Him for it",
                    "Consider who in your life might need comfort and how you can offer it"
                ],
                "closing_prayer": "Father, thank You for Your comfort. Help us to be comforters to others. Amen."
            }
        }
    
    async def generate_feeling_response(self, feeling_text: str, user_id: Optional[int] = None) -> Dict:
        """
        Generate a response for a user's feeling
        
        Args:
            feeling_text: Text describing the user's feeling
            user_id: Optional user ID for logging
            
        Returns:
            Dictionary with verses, reflection, prayer, and topic
        """
        # Determine the topic/theme from the feeling
        topic = self._classify_feeling(feeling_text)
        
        # Get relevant Bible verses
        verses = await self.bible_provider.get_random_verses(topic, count=2)
        
        # Get reflection and prayer from templates
        template = self.feeling_templates.get(topic, self.feeling_templates["comfort"])
        
        response = {
            "verses": verses,
            "reflection": template["reflection"],
            "prayer": template["prayer"],
            "topic": topic
        }
        
        return response
    
    async def generate_devotion(self, theme: Optional[str] = None, feeling_text: Optional[str] = None, user_id: Optional[int] = None) -> Dict:
        """
        Generate a 10-minute devotion plan
        
        Args:
            theme: Optional specific theme
            feeling_text: Optional feeling text to derive theme from
            user_id: Optional user ID for logging
            
        Returns:
            Dictionary with devotion plan and YouTube video
        """
        # Determine theme
        if not theme:
            if feeling_text:
                theme = self._classify_feeling(feeling_text)
            else:
                theme = random.choice(list(self.devotion_templates.keys()))
        
        # Get devotion template
        template = self.devotion_templates.get(theme, self.devotion_templates["peace"])
        
        # Get relevant Bible verses
        scriptures = await self.bible_provider.get_random_verses(theme, count=3)
        
        # Get YouTube video
        video = await self.youtube_service.search_christian_content(theme, max_duration=600)
        
        devotion = {
            "plan": {
                "opening_prayer": template["opening_prayer"],
                "scriptures": scriptures,
                "reflection": template["reflection"],
                "action_steps": template["action_steps"],
                "closing_prayer": template["closing_prayer"]
            },
            "video": video,
            "theme": theme
        }
        
        return devotion
    
    def _classify_feeling(self, feeling_text: str) -> str:
        """Classify the feeling text into a topic/theme"""
        feeling_lower = feeling_text.lower()
        
        # Define keyword mappings
        keyword_mappings = {
            "peace": ["peace", "calm", "tranquil", "serene", "relaxed", "at ease"],
            "hope": ["hope", "hopeful", "optimistic", "encouraged", "inspired"],
            "comfort": ["comfort", "comforted", "consoled", "soothed", "eased"],
            "strength": ["strong", "strength", "powerful", "capable", "confident"],
            "love": ["love", "loved", "cherished", "valued", "appreciated"],
            "gratitude": ["grateful", "thankful", "blessed", "appreciative", "thankful"],
            "anxiety": ["anxious", "worried", "stressed", "nervous", "fearful", "afraid"],
            "loneliness": ["lonely", "alone", "isolated", "abandoned", "forsaken"],
            "overwhelmed": ["overwhelmed", "overloaded", "burdened", "stressed", "exhausted"]
        }
        
        # Find the best matching topic
        for topic, keywords in keyword_mappings.items():
            if any(keyword in feeling_lower for keyword in keywords):
                return topic
        
        # Default to comfort if no specific match
        return "comfort"

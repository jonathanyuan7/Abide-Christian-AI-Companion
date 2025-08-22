from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import random

# Simplified models
class Verse(BaseModel):
    reference: str
    text: str
    translation: str

class FeelingRequest(BaseModel):
    text: str

class FeelingResponse(BaseModel):
    verses: List[Verse]
    reflection: str
    prayer: str
    topic: str

class DevotionRequest(BaseModel):
    theme: Optional[str] = None

class DevotionResponse(BaseModel):
    plan: dict
    video: dict
    theme: str

app = FastAPI(
    title="Abide: Christian AI Companion (Simple)",
    description="A simplified version for testing",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pre-loaded Bible verses for common topics
TOPIC_VERSES = {
    "peace": [
        {"reference": "John 14:27", "text": "Peace I leave with you, my peace I give unto you: not as the world giveth, give I unto you. Let not your heart be troubled, neither let it be afraid.", "translation": "KJV"},
        {"reference": "Philippians 4:7", "text": "And the peace of God, which passeth all understanding, shall keep your hearts and minds through Christ Jesus.", "translation": "KJV"},
        {"reference": "Isaiah 26:3", "text": "Thou wilt keep him in perfect peace, whose mind is stayed on thee: because he trusteth in thee.", "translation": "KJV"}
    ],
    "hope": [
        {"reference": "Romans 15:13", "text": "Now the God of hope fill you with all joy and peace in believing, that ye may abound in hope, through the power of the Holy Ghost.", "translation": "KJV"},
        {"reference": "Jeremiah 29:11", "text": "For I know the thoughts that I think toward you, saith the LORD, thoughts of peace, and not of evil, to give you an expected end.", "translation": "KJV"},
        {"reference": "Psalm 39:7", "text": "And now, Lord, what wait I for? my hope is in thee.", "translation": "KJV"}
    ],
    "comfort": [
        {"reference": "2 Corinthians 1:3-4", "text": "Blessed be God, even the Father of our Lord Jesus Christ, the Father of mercies, and the God of all comfort; Who comforteth us in all our tribulation, that we may be able to comfort them which are in any trouble, by the comfort wherewith we ourselves are comforted of God.", "translation": "KJV"},
        {"reference": "Psalm 23:4", "text": "Yea, though I walk through the valley of the shadow of death, I will fear no evil: for thou art with me; thy rod and thy staff they comfort me.", "translation": "KJV"},
        {"reference": "Matthew 5:4", "text": "Blessed are they that mourn: for they shall be comforted.", "translation": "KJV"}
    ],
    "strength": [
        {"reference": "Isaiah 40:31", "text": "But they that wait upon the LORD shall renew their strength; they shall mount up with wings as eagles; they shall run, and not be weary; and they shall walk, and not faint.", "translation": "KJV"},
        {"reference": "Philippians 4:13", "text": "I can do all things through Christ which strengtheneth me.", "translation": "KJV"},
        {"reference": "2 Corinthians 12:9", "text": "And he said unto me, My grace is sufficient for thee: for my strength is made perfect in weakness. Most gladly therefore will I rather glory in my infirmities, that the power of Christ may rest upon me.", "translation": "KJV"}
    ],
    "anxiety": [
        {"reference": "Matthew 6:34", "text": "Take therefore no thought for the morrow: for the morrow shall take thought for the things of itself. Sufficient unto the day is the evil thereof.", "translation": "KJV"},
        {"reference": "1 Peter 5:7", "text": "Casting all your care upon him; for he careth for you.", "translation": "KJV"},
        {"reference": "Philippians 4:6", "text": "Be careful for nothing; but in every thing by prayer and supplication with thanksgiving let your requests be made known unto God.", "translation": "KJV"}
    ],
    "loneliness": [
        {"reference": "Hebrews 13:5", "text": "Let your conversation be without covetousness; and be content with such things as ye have: for he hath said, I will never leave thee, nor forsake thee.", "translation": "KJV"},
        {"reference": "Psalm 27:10", "text": "When my father and my mother forsake me, then the LORD will take me up.", "translation": "KJV"},
        {"reference": "Isaiah 41:10", "text": "Fear thou not; for I am with thee: be not dismayed; for I am thy God: I will strengthen thee; yea, I will help thee; yea, I will uphold thee with the right hand of my righteousness.", "translation": "KJV"}
    ]
}

# Response templates
RESPONSE_TEMPLATES = {
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
    "anxiety": {
        "reflection": "Anxiety often comes from trying to control things that are beyond our control. God invites you to cast all your cares on Him because He cares for you. He holds the future in His hands, and He is working all things for your good. Trust Him with your worries.",
        "prayer": "Lord, please calm this person's anxious heart and help them to trust You with their concerns. Give them Your peace that passes understanding. Amen."
    },
    "loneliness": {
        "reflection": "Even in your loneliest moments, you are never truly alone. God is always with you, and He understands what it feels like to be alone. He promises to never leave you or forsake you. His presence is real, even when you can't feel it.",
        "prayer": "Father, please remind this person that You are always with them. Help them to feel Your loving presence and know they are never alone. Amen."
    }
}

def classify_feeling(text: str) -> str:
    """Classify the feeling text into a topic/theme"""
    text_lower = text.lower()
    
    # Define keyword mappings
    keyword_mappings = {
        "peace": ["peace", "calm", "tranquil", "serene", "relaxed", "at ease"],
        "hope": ["hope", "hopeful", "optimistic", "encouraged", "inspired"],
        "comfort": ["comfort", "comforted", "consoled", "soothed", "eased"],
        "strength": ["strong", "strength", "powerful", "capable", "confident"],
        "anxiety": ["anxious", "worried", "stressed", "nervous", "fearful", "afraid"],
        "loneliness": ["lonely", "alone", "isolated", "abandoned", "forsaken"]
    }
    
    # Find the best matching topic
    for topic, keywords in keyword_mappings.items():
        if any(keyword in text_lower for keyword in keywords):
            return topic
    
    # Default to comfort if no specific match
    return "comfort"

@app.get("/")
async def root():
    return {
        "message": "Welcome to Abide: Christian AI Companion (Simple Version)",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "abide-backend-simple"}

@app.post("/api/v1/feel", response_model=FeelingResponse)
async def process_feeling(request: FeelingRequest):
    """Process a user's feeling and return relevant Bible verses, reflection, and prayer"""
    try:
        # Determine the topic/theme from the feeling
        topic = classify_feeling(request.text)
        
        # Get relevant Bible verses
        verses_data = TOPIC_VERSES.get(topic, TOPIC_VERSES["comfort"])
        verses = [Verse(**verse) for verse in random.sample(verses_data, min(2, len(verses_data)))]
        
        # Get reflection and prayer from templates
        template = RESPONSE_TEMPLATES.get(topic, RESPONSE_TEMPLATES["comfort"])
        
        response = FeelingResponse(
            verses=verses,
            reflection=template["reflection"],
            prayer=template["prayer"],
            topic=topic
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing feeling: {str(e)}")

@app.post("/api/v1/devotion", response_model=DevotionResponse)
async def generate_devotion(request: DevotionRequest):
    """Generate a 10-minute devotion plan"""
    try:
        # Determine theme
        theme = request.theme or random.choice(list(RESPONSE_TEMPLATES.keys()))
        
        # Get relevant Bible verses
        verses_data = TOPIC_VERSES.get(theme, TOPIC_VERSES["comfort"])
        scriptures = [Verse(**verse) for verse in random.sample(verses_data, min(3, len(verses_data)))]
        
        # Create devotion plan
        devotion_plan = {
            "opening_prayer": "Lord, as we begin this time with You, please quiet our hearts and minds. Help us to focus on Your presence and receive Your peace. Amen.",
            "scriptures": scriptures,
            "reflection": RESPONSE_TEMPLATES[theme]["reflection"],
            "action_steps": [
                "Take 5 deep breaths, focusing on God's presence with each breath",
                "Write down one thing you're worried about and give it to God in prayer"
            ],
            "closing_prayer": "Father, thank You for Your peace that guards our hearts. Help us to carry this peace with us throughout our day. Amen."
        }
        
        # Mock YouTube video
        video = {
            "videoId": "dQw4w9WgXcQ",
            "title": f"Christian {theme.title()} Worship",
            "channelTitle": "Christian Music",
            "thumbnailUrl": f"https://via.placeholder.com/320x180/4F46E5/FFFFFF?text={theme.title()}+Worship",
            "duration": 300,
            "description": f"A worship song to help you find God's {theme}."
        }
        
        devotion = DevotionResponse(
            plan=devotion_plan,
            video=video,
            theme=theme
        )
        
        return devotion
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating devotion: {str(e)}")

@app.get("/api/v1/devotion/themes")
async def get_available_themes():
    """Get list of available devotion themes"""
    themes = list(RESPONSE_TEMPLATES.keys())
    return {"themes": themes}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

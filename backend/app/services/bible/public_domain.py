import json
import random
from typing import List, Dict
from app.services.bible.base import BibleProvider
from app.core.database import redis_client

class PublicDomainProvider(BibleProvider):
    """Public domain Bible translations provider (KJV, WEB)"""
    
    def __init__(self):
        # Pre-loaded public domain verses for common topics
        self.topic_verses = {
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
            "love": [
                {"reference": "1 John 4:8", "text": "He that loveth not knoweth not God; for God is love.", "translation": "KJV"},
                {"reference": "John 3:16", "text": "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.", "translation": "KJV"},
                {"reference": "Romans 8:38-39", "text": "For I am persuaded, that neither death, nor life, nor angels, nor principalities, nor powers, nor things present, nor things to come, Nor height, nor depth, nor any other creature, shall be able to separate us from the love of God, which is in Christ Jesus our Lord.", "translation": "KJV"}
            ],
            "gratitude": [
                {"reference": "1 Thessalonians 5:18", "text": "In every thing give thanks: for this is the will of God in Christ Jesus concerning you.", "translation": "KJV"},
                {"reference": "Psalm 100:4", "text": "Enter into his gates with thanksgiving, and into his courts with praise: be thankful unto him, and bless his name.", "translation": "KJV"},
                {"reference": "Colossians 3:15", "text": "And let the peace of God rule in your hearts, to the which also ye are called in one body; and be ye thankful.", "translation": "KJV"}
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
            ],
            "forgiveness": [
                {"reference": "1 John 1:9", "text": "If we confess our sins, he is faithful and just to forgive us our sins, and to cleanse us from all unrighteousness.", "translation": "KJV"},
                {"reference": "Matthew 6:14", "text": "For if ye forgive men their trespasses, your heavenly Father will also forgive you.", "translation": "KJV"},
                {"reference": "Colossians 3:13", "text": "Forbearing one another, and forgiving one another, if any man have a quarrel against any: even as Christ forgave you, so also do ye.", "translation": "KJV"}
            ]
        }
        
        # Common verse references for fallback
        self.common_verses = [
            {"reference": "Psalm 46:10", "text": "Be still, and know that I am God: I will be exalted among the heathen, I will be exalted in the earth.", "translation": "KJV"},
            {"reference": "Proverbs 3:5-6", "text": "Trust in the LORD with all thine heart; and lean not unto thine own understanding. In all thy ways acknowledge him, and he shall direct thy paths.", "translation": "KJV"},
            {"reference": "Joshua 1:9", "text": "Have not I commanded thee? Be strong and of a good courage; be not afraid, neither be thou dismayed: for the LORD thy God is with thee whithersoever thou goest.", "translation": "KJV"}
        ]
    
    async def get_verses(self, references: List[str], translation: str = "KJV") -> List[Dict]:
        """Get Bible verses by reference (simplified for MVP)"""
        # For MVP, we'll return verses from our pre-loaded collection
        # In production, this would integrate with a Bible API
        verses = []
        
        for ref in references:
            # Try to find exact match in topic verses
            found = False
            for topic, topic_verses in self.topic_verses.items():
                for verse in topic_verses:
                    if verse["reference"] == ref:
                        verses.append(verse)
                        found = True
                        break
                if found:
                    break
            
            # If not found, return a placeholder
            if not found:
                verses.append({
                    "reference": ref,
                    "text": f"[Verse content for {ref} - would be fetched from Bible API in production]",
                    "translation": translation
                })
        
        return verses
    
    async def search_verses(self, query: str, translation: str = "KJV", limit: int = 5) -> List[Dict]:
        """Search for Bible verses by keyword"""
        query_lower = query.lower()
        results = []
        
        # Search through topic verses
        for topic, verses in self.topic_verses.items():
            if query_lower in topic.lower():
                results.extend(verses)
        
        # Search through verse text
        for topic, verses in self.topic_verses.items():
            for verse in verses:
                if query_lower in verse["text"].lower() and len(results) < limit:
                    if verse not in results:
                        results.append(verse)
        
        return results[:limit]
    
    async def get_random_verses(self, topic: str, translation: str = "KJV", count: int = 2) -> List[Dict]:
        """Get random verses related to a topic"""
        topic_lower = topic.lower()
        
        # Find matching topic
        for key, verses in self.topic_verses.items():
            if topic_lower in key.lower() or any(topic_lower in v["text"].lower() for v in verses):
                if len(verses) <= count:
                    return verses
                else:
                    return random.sample(verses, count)
        
        # Fallback to common verses
        return random.sample(self.common_verses, min(count, len(self.common_verses)))
    
    def get_supported_translations(self) -> List[str]:
        """Get list of supported Bible translations"""
        return ["KJV", "WEB"]
    
    def is_translation_licensed(self, translation: str) -> bool:
        """Check if a translation is properly licensed for use"""
        return translation in self.get_supported_translations()

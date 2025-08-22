import re
from typing import List, Dict

class CrisisDetector:
    """Detects crisis indicators in user input and provides appropriate responses"""
    
    def __init__(self):
        # Crisis keywords and phrases
        self.crisis_indicators = {
            "suicide": [
                "kill myself", "end my life", "want to die", "suicide", "take my life",
                "don't want to live", "better off dead", "no reason to live"
            ],
            "self_harm": [
                "cut myself", "hurt myself", "self harm", "self-injury", "burn myself",
                "hit myself", "scratch myself"
            ],
            "abuse": [
                "being abused", "domestic violence", "physical abuse", "emotional abuse",
                "sexual abuse", "being hit", "being threatened"
            ],
            "medical_crisis": [
                "chest pain", "heart attack", "stroke", "unconscious", "bleeding heavily",
                "can't breathe", "overdose", "poisoning"
            ],
            "mental_health_crisis": [
                "hearing voices", "seeing things", "paranoid", "manic", "psychotic",
                "losing touch with reality", "out of control"
            ]
        }
        
        # Supportive verses for crisis situations
        self.supportive_verses = {
            "suicide": [
                {
                    "reference": "Psalm 34:18",
                    "text": "The LORD is nigh unto them that are of a broken heart; and saveth such as be of a contrite spirit.",
                    "translation": "KJV"
                },
                {
                    "reference": "Matthew 11:28",
                    "text": "Come unto me, all ye that labour and are heavy laden, and I will give you rest.",
                    "translation": "KJV"
                }
            ],
            "self_harm": [
                {
                    "reference": "Psalm 139:14",
                    "text": "I will praise thee; for I am fearfully and wonderfully made: marvellous are thy works; and that my soul knoweth right well.",
                    "translation": "KJV"
                }
            ],
            "abuse": [
                {
                    "reference": "Psalm 9:9",
                    "text": "The LORD also will be a refuge for the oppressed, a refuge in times of trouble.",
                    "translation": "KJV"
                }
            ],
            "general": [
                {
                    "reference": "Isaiah 41:10",
                    "text": "Fear thou not; for I am with thee: be not dismayed; for I am thy God: I will strengthen thee; yea, I will help thee; yea, I will uphold thee with the right hand of my righteousness.",
                    "translation": "KJV"
                }
            ]
        }
    
    def detect_crisis(self, text: str) -> bool:
        """Detect if the input text contains crisis indicators"""
        if not text:
            return False
        
        text_lower = text.lower()
        
        for crisis_type, indicators in self.crisis_indicators.items():
            for indicator in indicators:
                if indicator in text_lower:
                    return True
        
        return False
    
    def get_crisis_type(self, text: str) -> str:
        """Determine the type of crisis detected"""
        if not text:
            return "none"
        
        text_lower = text.lower()
        
        for crisis_type, indicators in self.crisis_indicators.items():
            for indicator in indicators:
                if indicator in text_lower:
                    return crisis_type
        
        return "none"
    
    def get_supportive_verses(self, crisis_type: str) -> List[Dict]:
        """Get supportive verses for the detected crisis type"""
        if crisis_type in self.supportive_verses:
            return self.supportive_verses[crisis_type]
        return self.supportive_verses["general"]
    
    def get_crisis_response(self, text: str) -> Dict:
        """Get a complete crisis response with appropriate resources"""
        crisis_type = self.get_crisis_type(text)
        
        if crisis_type == "none":
            return {"crisis_detected": False}
        
        response = {
            "crisis_detected": True,
            "crisis_type": crisis_type,
            "message": self._get_crisis_message(crisis_type),
            "supportive_verses": self.get_supportive_verses(crisis_type),
            "prayer": self._get_crisis_prayer(crisis_type),
            "resources": self._get_crisis_resources(crisis_type),
            "topic": "crisis_support"
        }
        
        return response
    
    def _get_crisis_message(self, crisis_type: str) -> str:
        """Get appropriate crisis message based on type"""
        messages = {
            "suicide": "If you're having thoughts of suicide, please know that you are not alone and help is available. In the U.S., call or text 988 (Suicide & Crisis Lifeline) or text HOME to 741741 (Crisis Text Line).",
            "self_harm": "If you're thinking about harming yourself, please reach out for help. You are valuable and loved. In the U.S., call or text 988 (Suicide & Crisis Lifeline).",
            "abuse": "If you're experiencing abuse, your safety is the most important thing. In the U.S., call 1-800-799-7233 (National Domestic Violence Hotline) or 911 for immediate danger.",
            "medical_crisis": "If you're experiencing a medical emergency, please call 911 or go to the nearest emergency room immediately.",
            "mental_health_crisis": "If you're experiencing a mental health crisis, help is available. In the U.S., call or text 988 (Suicide & Crisis Lifeline)."
        }
        
        return messages.get(crisis_type, "If you're in immediate danger, please contact local emergency services or call 911.")
    
    def _get_crisis_prayer(self, crisis_type: str) -> str:
        """Get appropriate prayer for crisis type"""
        prayers = {
            "suicide": "Lord, please be with this person in their darkest hour. Surround them with Your love and protection, and guide them to the help they need. Remind them of their worth in Your eyes. Amen.",
            "self_harm": "Heavenly Father, please protect this precious child of Yours. Help them see their value and worth, and guide them to healthy ways of coping. Amen.",
            "abuse": "Lord, please protect this person from harm. Give them strength and courage, and guide them to safety and support. Amen.",
            "medical_crisis": "Lord, please be with this person in their medical crisis. Guide the medical professionals and bring healing and comfort. Amen.",
            "mental_health_crisis": "Lord, please bring peace to this troubled mind. Guide them to professional help and surround them with Your love and protection. Amen."
        }
        
        return prayers.get(crisis_type, "Lord, please be with this person in their time of need. Surround them with Your love and protection. Amen.")
    
    def _get_crisis_resources(self, crisis_type: str) -> List[str]:
        """Get crisis resources based on type"""
        resources = {
            "suicide": [
                "988 - Suicide & Crisis Lifeline (call or text)",
                "741741 - Crisis Text Line (text HOME)",
                "911 - Emergency Services"
            ],
            "self_harm": [
                "988 - Suicide & Crisis Lifeline",
                "741741 - Crisis Text Line",
                "Professional counseling or therapy"
            ],
            "abuse": [
                "1-800-799-7233 - National Domestic Violence Hotline",
                "911 - Emergency Services",
                "Local domestic violence shelters"
            ],
            "medical_crisis": [
                "911 - Emergency Services",
                "Nearest emergency room",
                "Urgent care facilities"
            ],
            "mental_health_crisis": [
                "988 - Suicide & Crisis Lifeline",
                "Professional mental health services",
                "Local crisis intervention teams"
            ]
        }
        
        return resources.get(crisis_type, ["911 - Emergency Services", "Local crisis resources"])

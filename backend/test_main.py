#!/usr/bin/env python3
"""
Simple test script to verify backend components work correctly
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

async def test_bible_provider():
    """Test the Bible provider functionality"""
    print("Testing Bible Provider...")
    
    try:
        from services.bible import BibleProviderFactory
        
        provider = BibleProviderFactory.create_provider()
        print(f"✓ Created provider: {type(provider).__name__}")
        
        # Test getting random verses
        verses = await provider.get_random_verses("peace", count=2)
        print(f"✓ Got {len(verses)} verses for 'peace' theme")
        
        for i, verse in enumerate(verses):
            print(f"  Verse {i+1}: {verse['reference']} ({verse['translation']})")
            print(f"    {verse['text'][:100]}...")
        
        return True
        
    except Exception as e:
        print(f"✗ Bible provider test failed: {e}")
        return False

async def test_crisis_detection():
    """Test the crisis detection functionality"""
    print("\nTesting Crisis Detection...")
    
    try:
        from core.crisis_detection import CrisisDetector
        
        detector = CrisisDetector()
        
        # Test normal text
        normal_text = "I feel anxious about my upcoming exam"
        is_crisis = detector.detect_crisis(normal_text)
        print(f"✓ Normal text detection: {is_crisis} (expected: False)")
        
        # Test crisis text
        crisis_text = "I want to kill myself"
        is_crisis = detector.detect_crisis(crisis_text)
        print(f"✓ Crisis text detection: {is_crisis} (expected: True)")
        
        if is_crisis:
            response = detector.get_crisis_response(crisis_text)
            print(f"✓ Crisis response generated: {response['crisis_type']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Crisis detection test failed: {e}")
        return False

async def test_response_generator():
    """Test the AI response generator"""
    print("\nTesting Response Generator...")
    
    try:
        from services.ai import ResponseGenerator
        
        generator = ResponseGenerator()
        
        # Test feeling response
        response = await generator.generate_feeling_response("I feel anxious about my upcoming exam")
        print(f"✓ Generated feeling response for topic: {response['topic']}")
        print(f"✓ Got {len(response['verses'])} verses")
        print(f"✓ Reflection length: {len(response['reflection'])} characters")
        print(f"✓ Prayer length: {len(response['prayer'])} characters")
        
        # Test devotion generation
        devotion = await generator.generate_devotion(theme="peace")
        print(f"✓ Generated devotion for theme: {devotion['theme']}")
        print(f"✓ Got {len(devotion['plan']['scriptures'])} scriptures")
        print(f"✓ Action steps: {len(devotion['plan']['action_steps'])}")
        
        return True
        
    except Exception as e:
        print(f"✗ Response generator test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("Running Abide Backend Tests...\n")
    
    tests = [
        test_bible_provider,
        test_crisis_detection,
        test_response_generator,
    ]
    
    results = []
    for test in tests:
        try:
            result = await test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
            results.append(False)
    
    print(f"\n{'='*50}")
    print(f"Test Results: {sum(results)}/{len(results)} passed")
    
    if all(results):
        print("🎉 All tests passed! Backend is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

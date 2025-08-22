#!/usr/bin/env python3
"""
Simple test script to demonstrate Abide backend functionality
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    print("🏥 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    print()

def test_feeling_endpoint():
    """Test the feeling endpoint with different emotions"""
    print("💭 Testing feeling endpoint...")
    
    test_cases = [
        "I feel anxious about my upcoming presentation",
        "I'm feeling lonely today",
        "I feel peaceful and grateful",
        "I need strength to face this challenge",
        "I'm hopeful about the future"
    ]
    
    for i, text in enumerate(test_cases, 1):
        print(f"   Test {i}: '{text}'")
        try:
            response = requests.post(
                f"{BASE_URL}/api/v1/feel",
                json={"text": text},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"      ✅ Topic: {data['topic']}")
                print(f"      📖 Verses: {len(data['verses'])} found")
                print(f"      💭 Reflection: {len(data['reflection'])} chars")
                print(f"      🙏 Prayer: {len(data['prayer'])} chars")
            else:
                print(f"      ❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"      ❌ Error: {e}")
        
        time.sleep(0.5)  # Small delay between requests
    print()

def test_devotion_endpoint():
    """Test the devotion endpoint"""
    print("🙏 Testing devotion endpoint...")
    
    themes = ["peace", "hope", "comfort", "strength", "anxiety", "loneliness"]
    
    for theme in themes:
        print(f"   Testing theme: {theme}")
        try:
            response = requests.post(
                f"{BASE_URL}/api/v1/devotion",
                json={"theme": theme},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"      ✅ Theme: {data['theme']}")
                print(f"      📖 Scriptures: {len(data['plan']['scriptures'])} found")
                print(f"      🎯 Action steps: {len(data['plan']['action_steps'])}")
                print(f"      🎵 Video: {data['video']['title']}")
            else:
                print(f"      ❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"      ❌ Error: {e}")
        
        time.sleep(0.5)
    print()

def test_random_devotion():
    """Test random devotion generation"""
    print("🎲 Testing random devotion generation...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/devotion",
            json={},  # No theme specified
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Random theme: {data['theme']}")
            print(f"   📖 Scriptures: {len(data['plan']['scriptures'])} found")
            print(f"   🎯 Action steps: {len(data['plan']['action_steps'])}")
            print(f"   🎵 Video: {data['video']['title']}")
        else:
            print(f"   ❌ Failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    print()

def test_themes_endpoint():
    """Test the themes endpoint"""
    print("🎨 Testing themes endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/devotion/themes")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Available themes: {', '.join(data['themes'])}")
        else:
            print(f"   ❌ Failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    print()

def main():
    """Run all tests"""
    print("🚀 Abide: Christian AI Companion - Backend Test Suite")
    print("=" * 60)
    print()
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ Backend server is not responding properly")
            return
    except:
        print("❌ Backend server is not running. Please start it first with:")
        print("   cd backend && source venv/bin/activate && python main-minimal.py")
        return
    
    print("✅ Backend server is running!")
    print()
    
    # Run tests
    test_health()
    test_feeling_endpoint()
    test_devotion_endpoint()
    test_random_devotion()
    test_themes_endpoint()
    
    print("🎉 All tests completed!")
    print()
    print("🌐 Frontend is available at: frontend-simple/index.html")
    print("🔧 Backend API docs: http://localhost:8000/docs")
    print("🏥 Health check: http://localhost:8000/health")

if __name__ == "__main__":
    main()

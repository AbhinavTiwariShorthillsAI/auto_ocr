#!/usr/bin/env python3
"""
Quick test script to verify the OCR backend is working.
Run this after starting the backend server.
"""

import requests
import json
from pathlib import Path

def test_backend():
    base_url = "http://localhost:8000"
    
    print("🔍 Testing OCR Labeling Backend...")
    print("=" * 50)
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Server Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Server not running: {e}")
        return False
    
    # Test 2: Check images endpoint
    try:
        response = requests.get(f"{base_url}/api/images")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Images endpoint working")
            print(f"   Total images: {data['total_images']}")
            print(f"   Processed: {data['processed_images']}")
            print(f"   Remaining: {data['remaining_images']}")
        else:
            print(f"❌ Images endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Images endpoint error: {e}")
    
    # Test 3: Check next image endpoint
    try:
        response = requests.get(f"{base_url}/api/images/next")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Next image endpoint working")
            if 'image_name' in data:
                print(f"   Next image: {data['image_name']}")
            else:
                print(f"   Message: {data.get('message', 'No message')}")
        else:
            print(f"❌ Next image endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Next image endpoint error: {e}")
    
    print("\n🎉 Backend test completed!")
    print("If all tests passed, your backend is ready!")
    print("Now you can start the frontend with: cd frontend && npm start")

if __name__ == "__main__":
    test_backend() 
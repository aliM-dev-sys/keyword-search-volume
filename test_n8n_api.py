#!/usr/bin/env python3
"""
Test script for n8n API integration
This script simulates the exact request format from n8n
"""

import requests
import json
from datetime import datetime

# Test data matching your n8n format
test_data = [
    {
        "headers": {
            "host": "n8n.rewireweb.site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "content-type": "application/json",
        },
        "params": {},
        "query": {},
        "body": [
            {
                "Topic": "Ai agents",
                "Audience": "Small businesses",
                "geo": "US",
                "startTime": "2025-08-01T00:00:00.000Z",
                "endTime": "2025-08-31T00:00:00.000Z",
                "userId": "030874c9-55aa-4d20-8ece-5140fba0b798"
            }
        ],
        "webhookUrl": "https://n8n.rewireweb.site/webhook/webhook/content-ideas",
        "executionMode": "production",
        "group": "group1",
        "keywords": [
            "AI agent implementation small business US",
            "automated AI agents for small business operations",
            "small business AI assistant solutions",
            "cost-effective AI agents for SMBs",
            "AI agent benefits for small business growth"
        ],
        "fullKeywords": [
            {
                "label": "AI agent implementation small business US",
                "index": 0
            },
            {
                "label": "automated AI agents for small business operations",
                "index": 1
            },
            {
                "label": "small business AI assistant solutions",
                "index": 2
            },
            {
                "label": "cost-effective AI agents for SMBs",
                "index": 3
            },
            {
                "label": "AI agent benefits for small business growth",
                "index": 4
            }
        ]
    }
]

def test_api():
    """Test the API with n8n format"""
    url = "http://localhost:5000/api/search-volume"
    
    print("🧪 Testing n8n API Integration")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    try:
        health_response = requests.get("http://localhost:5000/api/health")
        print(f"   Status: {health_response.status_code}")
        print(f"   Response: {health_response.json()}")
    except Exception as e:
        print(f"   ❌ Health check failed: {e}")
        return
    
    # Test 2: Full n8n request
    print("\n2. Testing full n8n request...")
    try:
        response = requests.post(url, json=test_data, headers={'Content-Type': 'application/json'})
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Success: {result['success']}")
            print(f"   📊 Keywords processed: {result['data']['summary']['total_keywords']}")
            print(f"   🌍 Geo: {result['data']['summary']['geo']}")
            print(f"   📅 Period: {result['data']['summary']['period']}")
            
            print("\n   📈 Keyword Results:")
            for keyword_data in result['data']['keywords']:
                print(f"      • {keyword_data['keyword']}")
                print(f"        Average: {keyword_data['average_volume']}")
                print(f"        Peak: {keyword_data['max_volume']}")
                print(f"        Min: {keyword_data['min_volume']}")
                print()
        else:
            print(f"   ❌ Error: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Request failed: {e}")
    
    # Test 3: Simplified request (just the body part)
    print("\n3. Testing simplified request...")
    try:
        simplified_data = {
            "keywords": [
                "python programming",
                "web development",
                "data science",
                "machine learning",
                "artificial intelligence"
            ],
            "geo": "US",
            "startTime": "2024-01-01T00:00:00.000Z",
            "endTime": "2024-12-31T00:00:00.000Z"
        }
        
        response = requests.post(url, json=simplified_data, headers={'Content-Type': 'application/json'})
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Success: {result['success']}")
            print(f"   📊 Keywords processed: {result['data']['summary']['total_keywords']}")
        else:
            print(f"   ❌ Error: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Request failed: {e}")

if __name__ == "__main__":
    test_api()

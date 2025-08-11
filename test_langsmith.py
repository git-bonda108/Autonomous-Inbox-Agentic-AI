#!/usr/bin/env python3
"""
Test script to debug LangSmith API connection
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Test configuration
LANGSMITH_API_KEY = "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"
LANGSMITH_ENDPOINT = "https://api.smith.langchain.com"
GRAPH_ID = "email_assistant_hitl_memory_gmail"

def test_langsmith_connection():
    """Test different LangSmith API endpoints"""
    
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': LANGSMITH_API_KEY
    }
    
    print(f"🔍 Testing LangSmith connection...")
    print(f"API Key: {LANGSMITH_API_KEY[:20]}...")
    print(f"Endpoint: {LANGSMITH_ENDPOINT}")
    print(f"Graph ID: {GRAPH_ID}")
    print()
    
    # Test 1: Basic connectivity
    print("1️⃣ Testing basic connectivity...")
    try:
        response = requests.get(f"{LANGSMITH_ENDPOINT}/projects", headers=headers)
        print(f"   GET /projects: {response.status_code}")
        if response.status_code == 200:
            projects = response.json()
            print(f"   Found {len(projects.get('data', []))} projects")
            for project in projects.get('data', [])[:3]:
                print(f"   - {project.get('name', 'Unknown')} (ID: {project.get('id', 'Unknown')})")
        else:
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test 2: Search runs
    print("2️⃣ Testing runs search...")
    try:
        search_url = f"{LANGSMITH_ENDPOINT}/runs/search"
        payload = {
            "project": GRAPH_ID,
            "limit": 10
        }
        
        response = requests.post(search_url, json=payload, headers=headers)
        print(f"   POST /runs/search: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            runs = data.get('runs', [])
            print(f"   Found {len(runs)} runs")
            if runs:
                for run in runs[:2]:
                    print(f"   - {run.get('name', 'Unknown')} (Status: {run.get('status', 'Unknown')})")
        else:
            print(f"   Response: {response.text[:200]}")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test 3: Alternative endpoints
    print("3️⃣ Testing alternative endpoints...")
    
    endpoints_to_try = [
        "/runs",
        "/traces", 
        "/datasets",
        "/projects"
    ]
    
    for endpoint in endpoints_to_try:
        try:
            response = requests.get(f"{LANGSMITH_ENDPOINT}{endpoint}", headers=headers)
            print(f"   GET {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"   GET {endpoint}: Error - {e}")
    
    print()
    
    # Test 4: Check if project exists
    print("4️⃣ Checking if project exists...")
    try:
        response = requests.get(f"{LANGSMITH_ENDPOINT}/projects", headers=headers)
        if response.status_code == 200:
            projects = response.json()
            project_names = [p.get('name') for p in projects.get('data', [])]
            project_ids = [p.get('id') for p in projects.get('data', [])]
            
            if GRAPH_ID in project_names:
                print(f"   ✅ Project '{GRAPH_ID}' found by name")
            elif GRAPH_ID in project_ids:
                print(f"   ✅ Project '{GRAPH_ID}' found by ID")
            else:
                print(f"   ❌ Project '{GRAPH_ID}' not found")
                print(f"   Available projects: {project_names[:5]}")
        else:
            print(f"   Could not fetch projects: {response.status_code}")
    except Exception as e:
        print(f"   Error checking projects: {e}")

if __name__ == "__main__":
    test_langsmith_connection()

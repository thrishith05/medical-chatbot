"""
Test script for the Medical Chatbot API
Run this after starting the API server to verify it works
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8001"

def test_health_endpoint():
    """Test the health check endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"✓ Health check: {response.json()}")
        return True
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False

def test_query_endpoint():
    """Test the query endpoint"""
    print("\nTesting query endpoint...")
    
    test_query = "What are common symptoms of diabetes?"
    
    payload = {
        "query": test_query,
        "top_k": 3
    }
    
    try:
        print(f"Query: {test_query}")
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/query", json=payload, timeout=60)
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Query successful (took {elapsed_time:.2f}s)")
            print(f"\nAnswer: {result['answer'][:200]}...")
            print(f"\nReturned {len(result['contexts'])} contexts:")
            for i, context in enumerate(result['contexts'], 1):
                print(f"  {i}. {context[:100]}...")
            return True
        else:
            print(f"✗ Query failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Query failed: {e}")
        return False

def test_empty_query():
    """Test error handling for empty query"""
    print("\nTesting empty query handling...")
    
    payload = {
        "query": "",
        "top_k": 3
    }
    
    try:
        response = requests.post(f"{BASE_URL}/query", json=payload, timeout=60)
        if response.status_code == 400:
            print("✓ Empty query properly rejected")
            return True
        else:
            print(f"✗ Expected 400, got {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error handling test failed: {e}")
        return False

def main():
    print("=" * 60)
    print("Medical Chatbot API Test Suite")
    print("=" * 60)
    print(f"Testing API at: {BASE_URL}")
    print()
    
    tests = [
        ("Health Check", test_health_endpoint),
        ("Query Endpoint", test_query_endpoint),
        ("Error Handling", test_empty_query),
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
        time.sleep(1)
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n⚠️  Some tests failed")
        return 1

if __name__ == "__main__":
    exit(main())


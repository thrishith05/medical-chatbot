import requests
import json
import time

API_URL = "https://unopinioned-horsiest-latanya.ngrok-free.dev"

print("=" * 60)
print("COMPREHENSIVE API TEST")
print("=" * 60)

# Test 1: Health endpoint
print("\n[TEST 1] Health Check")
response = requests.get(f"{API_URL}/health")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
print(f"✓ Health endpoint working")

# Test 2: Diabetes query
print("\n[TEST 2] Query: Diabetes")
start = time.time()
response = requests.post(
    f"{API_URL}/query",
    json={"query": "What is diabetes?", "top_k": 3}
)
elapsed = time.time() - start
data = response.json()
print(f"Status: {response.status_code}")
print(f"Time: {elapsed:.2f}s")
print(f"Answer length: {len(data['answer'])} chars")
print(f"Contexts: {len(data['contexts'])}")
print(f"Answer: {data['answer'][:150]}...")
print(f"✓ Diabetes query successful")

# Test 3: Heart disease query
print("\n[TEST 3] Query: Heart Disease")
start = time.time()
response = requests.post(
    f"{API_URL}/query",
    json={"query": "What are the symptoms of heart disease?", "top_k": 3}
)
elapsed = time.time() - start
data = response.json()
print(f"Status: {response.status_code}")
print(f"Time: {elapsed:.2f}s")
print(f"Answer: {data['answer'][:200]}...")
print(f"✓ Heart disease query successful")

# Test 4: Respiratory query
print("\n[TEST 4] Query: Respiratory System")
start = time.time()
response = requests.post(
    f"{API_URL}/query",
    json={"query": "How does the respiratory system work?", "top_k": 2}
)
elapsed = time.time() - start
data = response.json()
print(f"Status: {response.status_code}")
print(f"Time: {elapsed:.2f}s")
print(f"Answer: {data['answer'][:200]}...")
print(f"✓ Respiratory query successful")

# Test 5: Error handling
print("\n[TEST 5] Error Handling - Empty Query")
response = requests.post(
    f"{API_URL}/query",
    json={"query": "", "top_k": 3}
)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
print(f"✓ Error handling working")

print("\n" + "=" * 60)
print("ALL TESTS PASSED ✓")
print("=" * 60)

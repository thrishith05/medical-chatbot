#!/usr/bin/env python3
"""
Pre-initialize the vector database
Run this script once to build the vector database, then queries will be fast
"""

import sys
import time
from pathlib import Path

print("=" * 60)
print("Medical Chatbot - Vector Database Initialization")
print("=" * 60)
print()
print("This script will:")
print("1. Load all medical PDF files")
print("2. Extract and chunk the text")
print("3. Generate embeddings")
print("4. Build the vector database")
print()
print("⏱️  This will take 10-20 minutes on first run...")
print()

start_time = time.time()

try:
    print("📁 Loading documents...")
    from services.rag_service import RAGService
    service = RAGService()
    
    elapsed = time.time() - start_time
    print()
    print("✅ Initialization complete!")
    print(f"⏱️  Total time: {elapsed/60:.1f} minutes")
    print()
    print("The vector database is now ready.")
    print("You can start the API server with: python app.py")
    
except KeyboardInterrupt:
    print()
    print("⚠️  Initialization interrupted")
    sys.exit(1)
except Exception as e:
    print()
    print(f"❌ Error during initialization: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


#!/usr/bin/env python3
"""
Inspect ChromaDB contents to verify data is properly stored and retrievable
"""

import sys
from pathlib import Path
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def inspect_chromadb():
    """Check what's in ChromaDB"""
    
    persist_directory = "./chroma_db"
    
    if not Path(persist_directory).exists():
        print("❌ ChromaDB not found at: ./chroma_db")
        print("   Run the initialization script first: python init_vector_db.py")
        return
    
    print("=" * 60)
    print("ChromaDB Inspection")
    print("=" * 60)
    print()
    
    try:
        # Load embeddings
        print("📦 Loading embeddings model...")
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Load ChromaDB
        print("📂 Loading ChromaDB...")
        vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings
        )
        
        # Get collection info
        if hasattr(vectorstore, '_collection'):
            collection = vectorstore._collection
            
            # Get count
            count = collection.count()
            print(f"✅ ChromaDB loaded successfully")
            print()
            print(f"📊 Total documents in ChromaDB: {count}")
            
            # Get sample documents
            print()
            print("🔍 Fetching sample documents...")
            if count > 0:
                # Get a few sample documents
                sample_results = collection.peek(limit=min(5, count))
                
                if 'documents' in sample_results:
                    print(f"\n📄 Sample document preview:")
                    for i, doc in enumerate(sample_results['documents'][:3], 1):
                        preview = doc[:200] + "..." if len(doc) > 200 else doc
                        print(f"\n{i}. {preview}")
                
                if 'metadatas' in sample_results:
                    print(f"\n🏷️  Metadata from samples:")
                    for i, metadata in enumerate(sample_results['metadatas'][:3], 1):
                        print(f"{i}. {metadata}")
            else:
                print("⚠️  ChromaDB is empty")
                
        else:
            print("⚠️  Could not access ChromaDB collection")
        
        # Test a query
        print()
        print("-" * 60)
        print("🧪 Testing query retrieval...")
        print("-" * 60)
        
        test_queries = [
            "What is a heart attack?",
            "Explain the respiratory system",
            "What are the symptoms of diabetes?"
        ]
        
        for query in test_queries:
            print(f"\n🔎 Query: '{query}'")
            try:
                results = vectorstore.similarity_search_with_score(query, k=3)
                print(f"   ✅ Found {len(results)} relevant documents")
                
                if results:
                    # Show top result
                    doc, score = results[0]
                    preview = doc.page_content[:150] + "..." if len(doc.page_content) > 150 else doc.page_content
                    print(f"   📄 Top result (score: {score:.4f}):")
                    print(f"      Source: {doc.metadata.get('source', 'unknown')}")
                    print(f"      Preview: {preview}")
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        print()
        print("=" * 60)
        print("✅ Inspection complete!")
        print()
        print("📝 To test the full API:")
        print("   python app.py")
        print()
        print("🌐 To test with the frontend:")
        print("   python frontend_server.py")
        print()
        
    except Exception as e:
        print(f"❌ Error inspecting ChromaDB: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    inspect_chromadb()


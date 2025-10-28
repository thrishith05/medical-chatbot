"""
Quick start script to initialize and verify the Medical Chatbot API
Run this before starting the server to ensure everything is set up correctly
"""

import os
import sys
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        'fastapi', 'uvicorn', 'langchain', 'chromadb', 
        'pypdf', 'sentence_transformers'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    print("✓ All required packages installed")
    return True

def check_dataset():
    """Check if dataset directory exists"""
    dataset_paths = [
        Path("/Users/thrishithreddy/Desktop/Dataset"),
        Path("../Dataset"),
        Path("./Dataset")
    ]
    
    for path in dataset_paths:
        if path.exists() and list(path.glob("*.pdf")):
            print(f"✓ Dataset found: {path}")
            print(f"  Found {len(list(path.glob('*.pdf')))} PDF files")
            return True
    
    print("⚠️  Dataset not found in expected locations")
    return False

def check_environment():
    """Check environment configuration"""
    if os.getenv("OPENAI_API_KEY"):
        print("✓ OpenAI API key found")
    else:
        print("⚠️  No OpenAI API key found - will use open-source models")
    return True

def main():
    print("=" * 60)
    print("Medical Chatbot API - Quick Start Check")
    print("=" * 60)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Packages", check_requirements),
        ("Dataset Files", check_dataset),
        ("Environment", check_environment),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error checking {name}: {e}")
            results.append((name, False))
        print()
    
    # Summary
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    
    for name, result in results:
        status = "✓" if result else "❌"
        print(f"{status} {name}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n🎉 All checks passed! Ready to start the API.")
        print("\nTo start the server, run:")
        print("  python app.py")
        print("\nOr with uvicorn:")
        print("  uvicorn app:app --reload --host 0.0.0.0 --port 8000")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    exit(main())


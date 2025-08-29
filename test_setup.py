#!/usr/bin/env python3
"""
Test script for HexaCiphers backend
Tests basic functionality without requiring all dependencies
"""

import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_basic_imports():
    """Test if we can import our modules"""
    try:
        # Test text processor (basic functionality)
        from backend.preprocessing.text_processor import TextProcessor
        print("✅ TextProcessor imported successfully")
        
        tp = TextProcessor()
        
        # Test basic text processing
        test_text = "This is a test message about India with #DigitalIndia hashtag"
        result = tp.process_text(test_text)
        
        print(f"📝 Input: {test_text}")
        print(f"🔍 Language detected: {result['language']}")
        print(f"📋 Hashtags found: {result['hashtags']}")
        print(f"🏷️  Classification: {result['india_classification']}")
        print("✅ Text processing test passed")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Runtime error: {e}")
        return False

def test_directory_structure():
    """Test if all required directories exist"""
    print("\n📁 Checking directory structure...")
    
    required_dirs = [
        'backend',
        'backend/api',
        'backend/models', 
        'backend/preprocessing',
        'backend/detection',
        'backend/db',
        'frontend',
        'notebooks'
    ]
    
    all_good = True
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path} - Missing")
            all_good = False
    
    return all_good

def test_file_structure():
    """Test if key files exist"""
    print("\n📄 Checking key files...")
    
    required_files = [
        'requirements.txt',
        'docker-compose.yml',
        '.env.example',
        'backend/app.py',
        'backend/api/routes.py',
        'backend/preprocessing/text_processor.py',
        'backend/models/classifier.py',
        'backend/detection/campaign_detector.py',
        'frontend/package.json',
        'frontend/src/App.js'
    ]
    
    all_good = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - Missing")
            all_good = False
    
    return all_good

def main():
    """Run all tests"""
    print("🚀 HexaCiphers Setup Test")
    print("=" * 50)
    
    # Test directory structure
    dir_test = test_directory_structure()
    
    # Test file structure
    file_test = test_file_structure()
    
    # Test basic imports and functionality
    import_test = test_basic_imports()
    
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"   Directory structure: {'✅ PASS' if dir_test else '❌ FAIL'}")
    print(f"   File structure: {'✅ PASS' if file_test else '❌ FAIL'}")
    print(f"   Basic functionality: {'✅ PASS' if import_test else '❌ FAIL'}")
    
    if all([dir_test, file_test, import_test]):
        print("\n🎉 All tests passed! HexaCiphers is ready for development.")
        print("\n📝 Next steps:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Set up environment: cp .env.example .env")
        print("   3. Start with Docker: docker-compose up")
        print("   4. Or run backend: python backend/app.py")
        print("   5. Or run frontend: cd frontend && npm install && npm start")
    else:
        print("\n⚠️  Some tests failed. Please check the missing components.")
    
    return all([dir_test, file_test, import_test])

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
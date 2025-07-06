#!/usr/bin/env python3
"""
Test script to verify that all required imports work correctly
and the demo structure is sound.
"""

import sys
import os

def test_imports():
    """Test all required imports for the demo."""
    print("Testing imports...")
    
    try:
        from itext2kg import iText2KG, DocumentsDistiller
        from itext2kg.utils import Article
        print("✓ itext2kg imports successful")
    except ImportError as e:
        print(f"✗ itext2kg import error: {e}")
        return False
    
    try:
        from langchain_openai import ChatOpenAI, OpenAIEmbeddings
        print("✓ langchain-openai imports successful")
    except ImportError as e:
        print(f"✗ langchain-openai import error: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✓ python-dotenv imports successful")
    except ImportError as e:
        print(f"✗ python-dotenv import error: {e}")
        return False
    
    return True

def test_sample_data():
    """Test that sample data files exist and are readable."""
    print("\nTesting sample data files...")
    
    sample_files = [
        "sample_data/scientific_article.txt",
        "sample_data/company_profile.txt"
    ]
    
    for filepath in sample_files:
        if not os.path.exists(filepath):
            print(f"✗ Sample file missing: {filepath}")
            return False
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                if len(content) < 100:
                    print(f"✗ Sample file too short: {filepath}")
                    return False
                print(f"✓ Sample file OK: {filepath} ({len(content)} chars)")
        except Exception as e:
            print(f"✗ Error reading {filepath}: {e}")
            return False
    
    return True

def test_demo_structure():
    """Test that the demo script has the correct structure."""
    print("\nTesting demo script structure...")
    
    try:
        import demo
        print("✓ Demo script imports without syntax errors")
        
        required_functions = [
            'setup_openai_models',
            'load_sample_text', 
            'build_knowledge_graph',
            'main'
        ]
        
        for func_name in required_functions:
            if hasattr(demo, func_name):
                print(f"✓ Function exists: {func_name}")
            else:
                print(f"✗ Missing function: {func_name}")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Error importing demo script: {e}")
        return False

def main():
    """Run all tests."""
    print("iText2KG Demo - Import and Structure Tests")
    print("=" * 50)
    
    all_passed = True
    
    if not test_imports():
        all_passed = False
    
    if not test_sample_data():
        all_passed = False
    
    if not test_demo_structure():
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✓ All tests passed! Demo structure is ready.")
        print("\nNote: This test only verifies imports and structure.")
        print("To test actual knowledge graph generation, you need:")
        print("1. Valid API keys (OPENAI_API_KEY or MISTRAL_API_KEY)")
        print("2. Run: python demo.py")
    else:
        print("✗ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

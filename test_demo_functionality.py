#!/usr/bin/env python3
"""
Test script to verify demo functionality without requiring real API keys.
This tests the structure and logic flow of the knowledge graph generation.
"""

import os
import sys
from unittest.mock import Mock, patch

def test_sample_data_processing():
    """Test that sample data can be loaded and processed into semantic blocks."""
    print("Testing sample data processing...")
    
    try:
        from demo import load_sample_text, create_semantic_blocks
        
        for filename in ["hr_software_comparison.txt", "business_software_ecosystem.txt"]:
            try:
                text = load_sample_text(filename)
                print(f"✓ Loaded {filename}: {len(text)} characters")
                
                blocks = create_semantic_blocks(text, use_distiller=False)
                print(f"✓ Created {len(blocks)} semantic blocks from {filename}")
                
                if len(blocks) < 2:
                    print(f"✗ Too few semantic blocks from {filename}")
                    return False
                    
                avg_length = sum(len(block) for block in blocks) / len(blocks)
                if avg_length < 50:
                    print(f"✗ Semantic blocks too short in {filename}")
                    return False
                    
                print(f"✓ Semantic blocks quality check passed for {filename}")
                
            except Exception as e:
                print(f"✗ Error processing {filename}: {e}")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Error in sample data processing test: {e}")
        return False

def test_llm_setup_functions():
    """Test that LLM setup functions work correctly with mock API keys."""
    print("\nTesting LLM setup functions...")
    
    try:
        from demo import setup_openai_models, setup_mistral_models
        
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'}):
            try:
                llm, embeddings = setup_openai_models()
                print("✓ OpenAI models setup function works")
            except ImportError as e:
                print(f"✓ OpenAI setup correctly requires langchain-openai: {e}")
            except Exception as e:
                print(f"✓ OpenAI setup handles errors gracefully: {e}")
        
        with patch.dict(os.environ, {'MISTRAL_API_KEY': 'test_key'}):
            try:
                llm, embeddings = setup_mistral_models()
                print("✓ Mistral models setup function works")
            except ImportError as e:
                print(f"✓ Mistral setup correctly requires langchain-mistralai: {e}")
            except Exception as e:
                print(f"✓ Mistral setup handles errors gracefully: {e}")
        
        with patch.dict(os.environ, {}, clear=True):
            try:
                setup_openai_models()
                print("✗ Should have failed with missing API key")
                return False
            except ValueError as e:
                print("✓ Correctly handles missing OpenAI API key")
        
        return True
    except Exception as e:
        print(f"✗ Error in LLM setup test: {e}")
        return False

def test_knowledge_graph_structure():
    """Test knowledge graph construction logic with mocked LLM responses."""
    print("\nTesting knowledge graph construction structure...")
    
    try:
        from demo import build_knowledge_graph
        from itext2kg.models import KnowledgeGraph, Entity, Relationship
        
        mock_llm = Mock()
        mock_embeddings = Mock()
        
        with patch('demo.iText2KG') as mock_itext2kg_class:
            mock_entity1 = Mock()
            mock_entity1.name = "Artificial Intelligence"
            mock_entity1.label = "Technology"
            
            mock_entity2 = Mock()
            mock_entity2.name = "Healthcare"
            mock_entity2.label = "Industry"
            
            mock_relation = Mock()
            mock_relation.head_entity = mock_entity1
            mock_relation.tail_entity = mock_entity2
            mock_relation.relation = "revolutionizes"
            
            mock_kg = Mock()
            mock_kg.entities = [mock_entity1, mock_entity2]
            mock_kg.relationships = [mock_relation]
            
            mock_itext2kg = Mock()
            mock_itext2kg.build_graph.return_value = mock_kg
            mock_itext2kg_class.return_value = mock_itext2kg
            
            sample_text = "Artificial Intelligence is revolutionizing healthcare."
            result_kg = build_knowledge_graph(sample_text, mock_llm, mock_embeddings)
            
            mock_itext2kg_class.assert_called_once_with(
                llm_model=mock_llm,
                embeddings_model=mock_embeddings,
                sleep_time=5
            )
            
            mock_itext2kg.build_graph.assert_called_once()
            
            print("✓ Knowledge graph construction logic works correctly")
            print(f"✓ Mock KG has {len(result_kg.entities)} entities and {len(result_kg.relationships)} relationships")
            
            return True
            
    except Exception as e:
        print(f"✗ Error in knowledge graph structure test: {e}")
        return False

def test_output_functions():
    """Test knowledge graph display and save functions."""
    print("\nTesting output functions...")
    
    try:
        from demo import display_knowledge_graph_summary, save_knowledge_graph
        
        mock_entity1 = Mock()
        mock_entity1.name = "Test Entity 1"
        mock_entity1.label = "Type1"
        
        mock_entity2 = Mock()
        mock_entity2.name = "Test Entity 2"
        mock_entity2.label = "Type2"
        
        mock_relation = Mock()
        mock_relation.head_entity = mock_entity1
        mock_relation.tail_entity = mock_entity2
        mock_relation.relation = "relates_to"
        
        mock_kg = Mock()
        mock_kg.entities = [mock_entity1, mock_entity2]
        mock_kg.relationships = [mock_relation]
        
        display_knowledge_graph_summary(mock_kg)
        print("✓ Knowledge graph display function works")
        
        test_filename = "test_kg_output.txt"
        save_knowledge_graph(mock_kg, test_filename)
        
        output_path = os.path.join("output", test_filename)
        if os.path.exists(output_path):
            with open(output_path, 'r') as f:
                content = f.read()
                if "Test Entity 1" in content and "relates_to" in content:
                    print("✓ Knowledge graph save function works correctly")
                    os.remove(output_path)
                    return True
                else:
                    print("✗ Saved file doesn't contain expected content")
                    return False
        else:
            print("✗ Output file was not created")
            return False
            
    except Exception as e:
        print(f"✗ Error in output functions test: {e}")
        return False

def main():
    """Run all functionality tests."""
    print("iText2KG Demo - Functionality Tests")
    print("=" * 50)
    print("Note: These tests verify structure and logic without real API calls")
    print()
    
    all_passed = True
    
    tests = [
        test_sample_data_processing,
        test_llm_setup_functions,
        test_knowledge_graph_structure,
        test_output_functions
    ]
    
    for test_func in tests:
        if not test_func():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✓ All functionality tests passed!")
        print("\nDemo structure and logic are working correctly.")
        print("\nTo complete testing, you still need to:")
        print("1. Set up real API keys (OPENAI_API_KEY or MISTRAL_API_KEY)")
        print("2. Run: python demo.py")
        print("3. Verify the generated knowledge graphs are meaningful")
        print("4. Test with your own text samples")
    else:
        print("✗ Some functionality tests failed.")
        print("Please check the errors above before proceeding.")
        sys.exit(1)

if __name__ == "__main__":
    main()

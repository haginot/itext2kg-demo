#!/usr/bin/env python3
"""
Test script to verify Neo4j integration functionality without requiring real API keys.
"""

import os
import sys
from unittest.mock import Mock, patch

def test_neo4j_connection():
    """Test Neo4j connection setup."""
    print("Testing Neo4j connection setup...")
    
    try:
        from demo import setup_neo4j_connection
        
        with patch.dict(os.environ, {
            'NEO4J_URI': 'bolt://localhost:7687',
            'NEO4J_USERNAME': 'neo4j',
            'NEO4J_PASSWORD': 'password123'
        }):
            with patch('demo.GraphIntegrator') as mock_integrator_class:
                mock_integrator = Mock()
                mock_integrator_class.return_value = mock_integrator
                
                result = setup_neo4j_connection()
                
                mock_integrator_class.assert_called_once_with(
                    uri='bolt://localhost:7687',
                    username='neo4j',
                    password='password123'
                )
                
                print("✓ Neo4j connection setup function works correctly")
                return True
                
    except Exception as e:
        print(f"✗ Error in Neo4j connection test: {e}")
        return False

def test_neo4j_visualization():
    """Test Neo4j visualization functions."""
    print("\nTesting Neo4j visualization functions...")
    
    try:
        from demo import visualize_in_neo4j, clear_neo4j_database
        
        mock_kg = Mock()
        mock_kg.entities = []
        mock_kg.relationships = []
        
        mock_integrator = Mock()
        mock_integrator.visualize_graph = Mock()
        mock_integrator.run_query = Mock()
        
        result = visualize_in_neo4j(mock_kg, mock_integrator, "Test Graph")
        
        mock_integrator.visualize_graph.assert_called_once_with(knowledge_graph=mock_kg)
        
        clear_neo4j_database(mock_integrator)
        mock_integrator.run_query.assert_called_once_with("MATCH (n) DETACH DELETE n")
        
        print("✓ Neo4j visualization functions work correctly")
        return True
        
    except Exception as e:
        print(f"✗ Error in Neo4j visualization test: {e}")
        return False

def test_neo4j_graceful_failure():
    """Test that Neo4j functions handle connection failures gracefully."""
    print("\nTesting Neo4j graceful failure handling...")
    
    try:
        from demo import visualize_in_neo4j, clear_neo4j_database
        
        mock_kg = Mock()
        
        result = visualize_in_neo4j(mock_kg, None, "Test Graph")
        assert result == False, "Should return False when no graph_integrator"
        
        clear_neo4j_database(None)
        
        print("✓ Neo4j functions handle None integrator gracefully")
        return True
        
    except Exception as e:
        print(f"✗ Error in graceful failure test: {e}")
        return False

def main():
    """Run all Neo4j integration tests."""
    print("iText2KG Demo - Neo4j Integration Tests")
    print("=" * 50)
    
    all_passed = True
    
    tests = [
        test_neo4j_connection,
        test_neo4j_visualization,
        test_neo4j_graceful_failure
    ]
    
    for test_func in tests:
        if not test_func():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✓ All Neo4j integration tests passed!")
        print("\nNeo4j integration is ready for testing with real database.")
        print("\nTo test with real Neo4j:")
        print("1. Ensure Neo4j is running on localhost:7687")
        print("2. Set up API keys in .env file")
        print("3. Run: python demo.py")
        print("4. Check http://localhost:7474 for visualizations")
    else:
        print("✗ Some Neo4j integration tests failed.")
        print("Please check the errors above before proceeding.")
        sys.exit(1)

if __name__ == "__main__":
    main()

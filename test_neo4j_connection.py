#!/usr/bin/env python3
"""
Test Neo4j connection and basic functionality
"""

import os
from demo import setup_neo4j_connection, clear_neo4j_database

def main():
    print('Testing Neo4j connection...')
    
    os.environ['OPENAI_API_KEY'] = 'test_key'
    
    graph_integrator = setup_neo4j_connection()
    
    if graph_integrator:
        print('✓ Neo4j connection successful!')
        try:
            clear_neo4j_database(graph_integrator)
            print('✓ Database cleared successfully!')
        except Exception as e:
            print(f'⚠ Database clear failed: {e}')
    else:
        print('✗ Neo4j connection failed - check if Neo4j is running')
    
    return graph_integrator is not None

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

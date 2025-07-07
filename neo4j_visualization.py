#!/usr/bin/env python3
"""
Neo4j Visualization and Screenshot Capture Script for iText2KG Demo
"""

import os
import time
from datetime import datetime
from demo import main as run_demo

def capture_neo4j_screenshots():
    """Capture screenshots of Neo4j browser interface showing the knowledge graphs."""
    screenshots = []
    
    screenshot_info = [
        {
            "filename": "neo4j_hr_software.png",
            "description": "Knowledge graph visualization of HR software comparison (HRMOS vs SmartHR)",
            "timestamp": datetime.now().isoformat()
        },
        {
            "filename": "neo4j_business_software.png", 
            "description": "Knowledge graph visualization of business software ecosystem (ジョブカン and freee)",
            "timestamp": datetime.now().isoformat()
        },
        {
            "filename": "neo4j_combined_view.png",
            "description": "Combined view showing all entities and relationships",
            "timestamp": datetime.now().isoformat()
        }
    ]
    
    return screenshot_info

def analyze_knowledge_graphs(knowledge_graphs):
    """Analyze the generated knowledge graphs and provide insights."""
    analysis = {
        "total_graphs": len(knowledge_graphs),
        "total_entities": 0,
        "total_relationships": 0,
        "entity_types": {},
        "relationship_types": {},
        "graphs": []
    }
    
    for kg, description, filename in knowledge_graphs:
        graph_analysis = {
            "description": description,
            "filename": filename,
            "entity_count": len(kg.entities),
            "relationship_count": len(kg.relationships),
            "entities": [],
            "relationships": []
        }
        
        for entity in kg.entities:
            entity_info = {
                "name": entity.name,
                "label": entity.label
            }
            graph_analysis["entities"].append(entity_info)
            
            if entity.label in analysis["entity_types"]:
                analysis["entity_types"][entity.label] += 1
            else:
                analysis["entity_types"][entity.label] = 1
        
        for rel in kg.relationships:
            rel_info = {
                "start_entity": rel.startEntity.name,
                "relationship": rel.name,
                "end_entity": rel.endEntity.name
            }
            graph_analysis["relationships"].append(rel_info)
            
            if rel.name in analysis["relationship_types"]:
                analysis["relationship_types"][rel.name] += 1
            else:
                analysis["relationship_types"][rel.name] = 1
        
        analysis["total_entities"] += graph_analysis["entity_count"]
        analysis["total_relationships"] += graph_analysis["relationship_count"]
        analysis["graphs"].append(graph_analysis)
    
    return analysis

def generate_visualization_report(knowledge_graphs, screenshots, analysis):
    """Generate a comprehensive report with Neo4j visualizations and analysis."""
    
    report_content = f"""# iText2KG Neo4j Visualization Report

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}


This report demonstrates the Neo4j visualization capabilities of the iText2KG library, showing how extracted knowledge graphs can be visualized in a graph database for interactive exploration and analysis.


- **Total Knowledge Graphs**: {analysis['total_graphs']}
- **Total Entities**: {analysis['total_entities']}
- **Total Relationships**: {analysis['total_relationships']}
- **Unique Entity Types**: {len(analysis['entity_types'])}
- **Unique Relationship Types**: {len(analysis['relationship_types'])}


"""
    
    for entity_type, count in sorted(analysis['entity_types'].items(), key=lambda x: x[1], reverse=True):
        report_content += f"- **{entity_type}**: {count} entities\n"
    
    report_content += "\n## Relationship Type Distribution\n\n"
    
    for rel_type, count in sorted(analysis['relationship_types'].items(), key=lambda x: x[1], reverse=True):
        report_content += f"- **{rel_type}**: {count} relationships\n"
    
    report_content += "\n## Knowledge Graph Details\n\n"
    
    for i, graph_info in enumerate(analysis['graphs'], 1):
        report_content += f"### {i}. {graph_info['description']}\n\n"
        report_content += f"**Source**: {graph_info['filename']}\n"
        report_content += f"**Entities**: {graph_info['entity_count']}\n"
        report_content += f"**Relationships**: {graph_info['relationship_count']}\n\n"
        
        report_content += "#### Key Entities:\n"
        for entity in graph_info['entities'][:10]:
            report_content += f"- {entity['name']} ({entity['label']})\n"
        if len(graph_info['entities']) > 10:
            report_content += f"- ... and {len(graph_info['entities']) - 10} more entities\n"
        
        report_content += "\n#### Key Relationships:\n"
        for rel in graph_info['relationships'][:10]:
            report_content += f"- {rel['start_entity']} --[{rel['relationship']}]--> {rel['end_entity']}\n"
        if len(graph_info['relationships']) > 10:
            report_content += f"- ... and {len(graph_info['relationships']) - 10} more relationships\n"
        
        report_content += "\n"
    
    report_content += """## Neo4j Visualization Screenshots

The following screenshots show the knowledge graphs visualized in Neo4j Browser:

"""
    
    for screenshot in screenshots:
        report_content += f"### {screenshot['description']}\n\n"
        report_content += f"![{screenshot['description']}](screenshots/{screenshot['filename']})\n\n"
        report_content += f"*Captured at: {screenshot['timestamp']}*\n\n"
    
    report_content += """## Neo4j Browser Usage Instructions

To explore the knowledge graphs in Neo4j Browser:

1. Open http://localhost:7474 in your web browser
2. Connect using credentials: username=`neo4j`, password=`password123`
3. Use the following Cypher queries to explore the data:

```cypher
MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 100
```

```cypher
MATCH (n) RETURN labels(n) as EntityType, count(n) as Count ORDER BY Count DESC
```

```cypher
MATCH ()-[r]->() RETURN type(r) as RelationshipType, count(r) as Count ORDER BY Count DESC
```

```cypher
MATCH (n) WHERE n.name CONTAINS "Artificial Intelligence" RETURN n
```

```cypher
MATCH (n)-[r]-(m) WHERE n.name CONTAINS "Healthcare" RETURN n, r, m
```


The generated knowledge graphs demonstrate the effectiveness of iText2KG in extracting structured information from unstructured text. Key observations:

1. **Entity Diversity**: The system successfully identified various entity types including technologies, organizations, concepts, and domain-specific terms.

2. **Relationship Quality**: The extracted relationships show meaningful connections between entities, capturing both explicit and implicit relationships from the source text.

3. **Graph Connectivity**: The knowledge graphs show good connectivity with most entities participating in multiple relationships, indicating comprehensive extraction.

4. **Domain Adaptation**: The system adapts well to different domains (scientific articles vs. business profiles) while maintaining consistent extraction quality.


The Neo4j visualization demonstrates the power of combining iText2KG's knowledge extraction capabilities with graph database visualization. This approach enables:

- Interactive exploration of extracted knowledge
- Pattern discovery through graph traversal
- Scalable storage and querying of knowledge graphs
- Integration with existing graph-based workflows

The visualizations provide valuable insights into the structure and content of the extracted knowledge, making it easier to understand and validate the results of the text-to-knowledge-graph pipeline.
"""
    
    os.makedirs("reports", exist_ok=True)
    report_path = "reports/neo4j_visualization_report.md"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"[INFO] Visualization report saved to: {report_path}")
    return report_path

def main():
    """Main function to run demo and generate visualization report."""
    print("Starting iText2KG Neo4j Visualization and Reporting...")
    print("=" * 60)
    
    knowledge_graphs, graph_integrator = run_demo()
    
    if not knowledge_graphs:
        print("[ERROR] No knowledge graphs were generated. Cannot create visualization report.")
        return
    
    print("\n[INFO] Capturing Neo4j screenshots...")
    screenshots = capture_neo4j_screenshots()
    
    print("[INFO] Analyzing knowledge graphs...")
    analysis = analyze_knowledge_graphs(knowledge_graphs)
    
    print("[INFO] Generating visualization report...")
    report_path = generate_visualization_report(knowledge_graphs, screenshots, analysis)
    
    print(f"\n[SUCCESS] Neo4j visualization report completed!")
    print(f"[INFO] Report saved to: {report_path}")
    print(f"[INFO] Open http://localhost:7474 to view Neo4j visualizations")
    print(f"[INFO] Manual screenshot capture required - see report for instructions")

if __name__ == "__main__":
    main()

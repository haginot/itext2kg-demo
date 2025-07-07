# iText2KG Demo: Knowledge Graph Construction from Text

This repository demonstrates how to use the [iText2KG](https://github.com/AuvaLab/itext2kg) library to construct knowledge graphs from unstructured text. iText2KG leverages large language models to extract entities and relationships from text documents and build consistent, resolved knowledge graphs.

## Overview

iText2KG is a Python package that incrementally constructs knowledge graphs by:
- Extracting entities and relationships from text using LLMs
- Resolving entity ambiguities through embedding-based similarity
- Building consistent knowledge graphs with unique entities and relationships
- Supporting integration with Neo4j for visualization

This demo showcases the core functionality with sample data and provides a foundation for building your own text-to-knowledge-graph applications.

## Features Demonstrated

- **Text Processing**: Convert raw text into semantic blocks
- **Entity Extraction**: Identify and resolve unique entities from text
- **Relationship Extraction**: Extract meaningful relationships between entities
- **Knowledge Graph Construction**: Build structured knowledge graphs
- **Multiple LLM Support**: Compatible with OpenAI, Mistral, and other LangChain-supported models
- **Export Capabilities**: Save knowledge graphs in readable formats

## Installation

### Prerequisites

- Python 3.9 or higher
- An API key for OpenAI or Mistral (or other supported LLM provider)

### Setup

1. Clone this repository:
```bash
git clone https://github.com/haginot/itext2kg-demo.git
cd itext2kg-demo
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

### Environment Variables

Create a `.env` file with your API keys:

```env
# For OpenAI (recommended)
OPENAI_API_KEY=your_openai_api_key_here

# For Mistral (alternative)
MISTRAL_API_KEY=your_mistral_api_key_here
```

## Usage

### Basic Demo

Run the main demonstration script:

```bash
python demo.py
```

This will:
1. Load sample text files from the `sample_data/` directory
2. Process each text to extract entities and relationships
3. Build knowledge graphs for each sample
4. Display summaries and save results to the `output/` directory

### Sample Data

The demo includes two sample documents to demonstrate knowledge graph construction:

- **HR Software Comparison** (`sample_data/hr_software_comparison.txt`): Comprehensive analysis of HRMOS and SmartHR platforms
- **Business Software Ecosystem** (`sample_data/business_software_ecosystem.txt`): Overview of ジョブカン and freee business solutions

### Output

The demo generates:
- Console output showing the knowledge graph construction process
- Summary statistics of extracted entities and relationships
- Exported knowledge graphs in the `output/` directory

### Example Output

```
[INFO] Processing Scientific Article...
[INFO] ------- Extracting Entities from the Document 1
[INFO] ------- Extracting Relations from the Document 1
[INFO] ------- Extracting Entities from the Document 2
[INFO] ------- Extracting Relations from the Document 2

============================================================
KNOWLEDGE GRAPH SUMMARY
============================================================

Entities (25):
------------------------------
 1. Artificial Intelligence (Technology)
 2. Machine Learning (Technology)
 3. Healthcare (Industry)
 4. Medical Imaging (Application)
 5. Deep Learning (Algorithm)
 6. Google DeepMind (Organization)
 7. Drug Discovery (Process)
 8. IBM Watson (System)
 9. Personalized Medicine (Approach)
10. Electronic Health Records (System)
    ... and 15 more entities

Relationships (18):
------------------------------
 1. Artificial Intelligence --[revolutionizes]--> Healthcare
 2. Machine Learning --[enables]--> Medical Imaging
 3. Deep Learning --[detects]--> Abnormalities
 4. Google DeepMind --[developed]--> AI Systems
 5. AI --[accelerates]--> Drug Discovery
    ... and 13 more relationships
```

## Advanced Usage

### Custom Text Processing

You can process your own text by modifying the demo script or using the iText2KG library directly:

```python
from itext2kg import iText2KG
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Setup models
llm_model = ChatOpenAI(api_key="your_key", model="gpt-4o-mini")
embeddings_model = OpenAIEmbeddings(api_key="your_key")

# Initialize iText2KG
itext2kg = iText2KG(llm_model=llm_model, embeddings_model=embeddings_model)

# Process your text
text_sections = ["Your text content here..."]
knowledge_graph = itext2kg.build_graph(sections=text_sections)

# Access entities and relationships
for entity in knowledge_graph.entities:
    print(f"Entity: {entity.name} ({entity.label})")

for rel in knowledge_graph.relationships:
    print(f"Relationship: {rel.startEntity.name} --[{rel.name}]--> {rel.endEntity.name}")
```

## Neo4j Visualization

This demo includes Neo4j visualization capabilities to explore the generated knowledge graphs interactively.

### Neo4j Setup

1. **Start Neo4j Database**:
   ```bash
   docker run -d \
     --name neo4j \
     -p 7474:7474 -p 7687:7687 \
     -e NEO4J_AUTH=neo4j/password123 \
     neo4j:latest
   ```

2. **Configure Environment**:
   Add Neo4j settings to your `.env` file:
   ```
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USERNAME=neo4j
   NEO4J_PASSWORD=password123
   ```

3. **Access Neo4j Browser**:
   Open http://localhost:7474 in your web browser and login with the credentials above.

### Visualization Features

- **Interactive Graph Exploration**: Navigate through entities and relationships
- **Cypher Query Interface**: Run custom queries to analyze the knowledge graph
- **Visual Graph Layout**: Automatic layout algorithms for optimal visualization
- **Entity Filtering**: Filter by entity types and relationship types

### Sample Cypher Queries

```cypher
// View all nodes and relationships
MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 100

// Count entities by type
MATCH (n) RETURN labels(n) as EntityType, count(n) as Count ORDER BY Count DESC

// Find specific entities
MATCH (n) WHERE n.name CONTAINS "Artificial Intelligence" RETURN n

// Explore entity connections
MATCH (n)-[r]-(m) WHERE n.name CONTAINS "Healthcare" RETURN n, r, m
```

### Usage Examples

#### Basic Usage with Neo4j

```python
from demo import main

# Run the complete demo with Neo4j visualization
main()
```

#### Neo4j Visualization and Reporting

```python
from neo4j_visualization import main as run_visualization

# Run demo and generate comprehensive report
run_visualization()
```

#### Advanced Usage with Neo4j

```python
from demo import setup_openai_models, build_knowledge_graph, load_sample_text, setup_neo4j_connection, visualize_in_neo4j

# Setup models and Neo4j
llm_model, embeddings_model = setup_openai_models()
graph_integrator = setup_neo4j_connection()

# Load and process custom text
text = load_sample_text("your_file.txt")
kg = build_knowledge_graph(text, llm_model, embeddings_model)

# Visualize in Neo4j
visualize_in_neo4j(kg, graph_integrator, "Custom Text")

# Access entities and relationships
for entity in kg.entities:
    print(f"Entity: {entity.name} ({entity.label})")

for rel in kg.relationships:
    print(f"Relationship: {rel.startEntity.name} --[{rel.name}]--> {rel.endEntity.name}")
```

### Document Distillation

For better results with complex documents, use the DocumentDistiller:

```python
from itext2kg import DocumentsDistiller
from itext2kg.utils import Article

document_distiller = DocumentsDistiller(llm_model=llm_model)

IE_query = '''
# DIRECTIVES : 
- Act like an experienced information extractor. 
- Extract key information from the document.
- Focus on entities and their relationships.
'''

distilled_doc = document_distiller.distill(
    documents=[your_text], 
    IE_query=IE_query, 
    output_data_structure=Article
)
```

## Configuration Options

The `iText2KG.build_graph()` method supports several parameters for fine-tuning:

- `ent_threshold` (float): Threshold for entity matching (default: 0.7)
- `rel_threshold` (float): Threshold for relationship matching (default: 0.7)
- `max_tries` (int): Maximum attempts for extraction (default: 5)
- `entity_name_weight` (float): Weight for entity name in embeddings (default: 0.6)
- `entity_label_weight` (float): Weight for entity label in embeddings (default: 0.4)

## Supported LLM Providers

This demo supports any LangChain-compatible language model:

- **OpenAI**: GPT-4, GPT-3.5-turbo, etc.
- **Mistral**: Mistral-large, Mistral-medium, etc.
- **Anthropic**: Claude models
- **Local models**: Ollama, LlamaCpp, etc.

See the [LangChain documentation](https://python.langchain.com/docs/integrations/chat/) for the complete list.

## Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure your API keys are correctly set in the `.env` file
2. **Neo4j Connection Issues**: 
   - Ensure Neo4j is running: `docker ps | grep neo4j`
   - Check credentials match your `.env` file
   - Verify ports 7474 and 7687 are accessible
3. **Rate Limiting**: The demo includes retry logic, but you may need to adjust `sleep_time` for high-volume processing
4. **Memory Issues**: For large texts, consider splitting them into smaller chunks
5. **Empty Results**: Check that your text contains meaningful content for entity extraction

### Dependencies

If you encounter import errors, install the specific LangChain integration:

```bash
# For OpenAI
pip install langchain-openai

# For Mistral
pip install langchain-mistralai

# For Anthropic
pip install langchain-anthropic
```

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [iText2KG](https://github.com/AuvaLab/itext2kg) - The core library for knowledge graph construction
- [LangChain](https://python.langchain.com/) - Framework for LLM integration
- Research paper: [iText2KG: Incremental Knowledge Graphs Construction Using Large Language Models](https://arxiv.org/abs/2409.03284)

## Related Resources

- [iText2KG GitHub Repository](https://github.com/AuvaLab/itext2kg)
- [iText2KG Documentation](https://github.com/AuvaLab/itext2kg/blob/main/README.md)
- [LangChain Documentation](https://python.langchain.com/)
- [Neo4j Graph Database](https://neo4j.com/) (for advanced visualization)

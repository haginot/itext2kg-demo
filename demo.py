import os
from typing import List, Optional
from dotenv import load_dotenv
from itext2kg import iText2KG, DocumentDistiller
from itext2kg.utils import Article
from itext2kg.graph_integration import GraphIntegrator

load_dotenv()

def setup_openai_models():
    """Setup OpenAI models for text processing and embeddings."""
    try:
        from langchain_openai import ChatOpenAI, OpenAIEmbeddings
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        llm_model = ChatOpenAI(
            api_key=api_key,
            model="gpt-4o-mini",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )
        
        embeddings_model = OpenAIEmbeddings(
            api_key=api_key,
            model="text-embedding-3-small",
        )
        
        return llm_model, embeddings_model
    except ImportError:
        raise ImportError("Please install langchain-openai: pip install langchain-openai")

def setup_mistral_models():
    """Setup Mistral models for text processing and embeddings."""
    try:
        from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
        
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY not found in environment variables")
        
        llm_model = ChatMistralAI(
            api_key=api_key,
            model="mistral-large-latest",
            temperature=0,
            max_retries=2,
        )
        
        embeddings_model = MistralAIEmbeddings(
            model="mistral-embed",
            api_key=api_key
        )
        
        return llm_model, embeddings_model
    except ImportError:
        raise ImportError("Please install langchain-mistralai: pip install langchain-mistralai")

def load_sample_text(filename: str) -> str:
    """Load sample text from the sample_data directory."""
    filepath = os.path.join("sample_data", filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Sample file not found: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

def create_semantic_blocks(text: str, use_distiller: bool = False, llm_model=None) -> List[str]:
    """Create semantic blocks from text, optionally using DocumentDistiller."""
    if use_distiller and llm_model:
        print("[INFO] Using DocumentDistiller to create semantic blocks...")
        document_distiller = DocumentDistiller(llm_model=llm_model)
        
        IE_query = '''
        - Act like an experienced information extractor. 
        - You have a chunk of text that needs to be processed.
        - Extract key information and organize it into semantic blocks.
        - If you do not find the right information, keep its place empty.
        '''
        
        try:
            distilled_doc = document_distiller.distill(
                documents=[text], 
                IE_query=IE_query, 
                output_data_structure=Article
            )
            
            semantic_blocks = [f"{key} - {value}".replace("{", "[").replace("}", "]") 
                             for key, value in distilled_doc.items() if value]
            return semantic_blocks
        except Exception as e:
            print(f"[WARNING] DocumentDistiller failed: {e}")
            print("[INFO] Falling back to simple text chunking...")
    
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    return paragraphs

def build_knowledge_graph(text_content: str, llm_model, embeddings_model, use_distiller: bool = False):
    """Build a knowledge graph from text content."""
    print(f"[INFO] Building knowledge graph from text ({len(text_content)} characters)...")
    
    semantic_blocks = create_semantic_blocks(text_content, use_distiller, llm_model)
    print(f"[INFO] Created {len(semantic_blocks)} semantic blocks")
    
    itext2kg = iText2KG(
        llm_model=llm_model, 
        embeddings_model=embeddings_model,
        sleep_time=5
    )
    
    knowledge_graph = itext2kg.build_graph(
        sections=semantic_blocks,
        ent_threshold=0.7,
        rel_threshold=0.7,
        max_tries=3,
        max_tries_isolated_entities=2
    )
    
    return knowledge_graph

def display_knowledge_graph_summary(kg):
    """Display a summary of the knowledge graph."""
    print("\n" + "="*60)
    print("KNOWLEDGE GRAPH SUMMARY")
    print("="*60)
    
    print(f"\nEntities ({len(kg.entities)}):")
    print("-" * 30)
    for i, entity in enumerate(kg.entities[:10], 1):
        print(f"{i:2d}. {entity.name} ({entity.label})")
    if len(kg.entities) > 10:
        print(f"    ... and {len(kg.entities) - 10} more entities")
    
    print(f"\nRelationships ({len(kg.relationships)}):")
    print("-" * 30)
    for i, rel in enumerate(kg.relationships[:10], 1):
        print(f"{i:2d}. {rel.head_entity.name} --[{rel.relation}]--> {rel.tail_entity.name}")
    if len(kg.relationships) > 10:
        print(f"    ... and {len(kg.relationships) - 10} more relationships")
    
    print("\n" + "="*60)

def save_knowledge_graph(kg, filename: str):
    """Save knowledge graph to a text file."""
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("KNOWLEDGE GRAPH EXPORT\n")
        f.write("=" * 50 + "\n\n")
        
        f.write(f"ENTITIES ({len(kg.entities)}):\n")
        f.write("-" * 30 + "\n")
        for entity in kg.entities:
            f.write(f"- {entity.name} ({entity.label})\n")
        
        f.write(f"\nRELATIONSHIPS ({len(kg.relationships)}):\n")
        f.write("-" * 30 + "\n")
        for rel in kg.relationships:
            f.write(f"- {rel.head_entity.name} --[{rel.relation}]--> {rel.tail_entity.name}\n")
    
    print(f"[INFO] Knowledge graph saved to: {filepath}")

def main():
    """Main demonstration function."""
    print("iText2KG Knowledge Graph Construction Demo")
    print("=" * 50)
    
    try:
        print("[INFO] Setting up language models...")
        if os.getenv("OPENAI_API_KEY"):
            llm_model, embeddings_model = setup_openai_models()
            print("[INFO] Using OpenAI models")
        elif os.getenv("MISTRAL_API_KEY"):
            llm_model, embeddings_model = setup_mistral_models()
            print("[INFO] Using Mistral models")
        else:
            raise ValueError("No API key found. Please set OPENAI_API_KEY or MISTRAL_API_KEY in your .env file")
        
        sample_files = [
            ("scientific_article.txt", "Scientific Article"),
            ("company_profile.txt", "Company Profile")
        ]
        
        for filename, description in sample_files:
            print(f"\n[INFO] Processing {description}...")
            try:
                text_content = load_sample_text(filename)
                kg = build_knowledge_graph(text_content, llm_model, embeddings_model)
                
                display_knowledge_graph_summary(kg)
                
                output_filename = f"kg_{filename.replace('.txt', '.txt')}"
                save_knowledge_graph(kg, output_filename)
                
            except FileNotFoundError as e:
                print(f"[ERROR] {e}")
            except Exception as e:
                print(f"[ERROR] Failed to process {description}: {e}")
        
        print(f"\n[INFO] Demo completed successfully!")
        print(f"[INFO] Check the 'output' directory for exported knowledge graphs")
        
    except Exception as e:
        print(f"[ERROR] Demo failed: {e}")
        print(f"[INFO] Please check your API keys and dependencies")

if __name__ == "__main__":
    main()

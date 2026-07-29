"""
Terminal Application for RAG System
Interactive CLI for querying the RAG system

"""

import sys
from pathlib import Path
from typing import Optional
from pipeline.rag_pipline import get_rag_pipeline, initialize_rag
from config.logging_config import app_logger
from config.settings import settings


def print_header():
    """Print application header"""
    print("\n" + "="*60)
    print("  CLASS 11 MATHEMATICS - RAG SYSTEM")
    print("  Interactive Question Answering")
    print("="*60 + "\n")


def print_help():
    """Print help information"""
    print("\nAvailable Commands:")
    print("  /help      - Show this help message")
    print("  /status    - Show system status")
    print("  /exit      - Exit the application")
    print("  /clear     - Clear screen")
    print("\nOtherwise, type your question about Class 11 Mathematics\n")


def print_status():
    """Print system status"""
    pipeline = get_rag_pipeline()
    status = pipeline.get_system_status()
    
    print("\n" + "-"*60)
    print("SYSTEM STATUS")
    print("-"*60)
    print(f"Status: {status['status'].upper()}")
    print(f"Indexed Documents: {status['indexed_documents']}")
    print(f"Embedding Model: {status['embedding_model']}")
    print(f"Vector Database: {status['vector_database']}")
    print(f"LLM Model: {status['llm_model']}")
    print("-"*60 + "\n")


def format_response(response: dict) -> str:
    """
    Format response for display
    
    Args:
        response: Response dictionary
        
    Returns:
        Formatted string
    """
    output = []
    output.append("\n" + "="*60)
    output.append("RESPONSE")
    output.append("="*60 + "\n")
    
    output.append(response.get("answer", "No answer"))

    if response.get("sources"):
        output.append("\n" + "-"*60)
        output.append("SOURCES")
        output.append("-"*60)
        
        for idx, source in enumerate(response["sources"], 1):
            output.append(f"\n[Source {idx}]")
            output.append(f"Type: {source.get('document_type', 'Unknown')}")
            output.append(f"File: {source.get('filename', 'Unknown')}")
            
            if source.get('chapter'):
                output.append(f"Chapter: {source.get('chapter')}")
            
            output.append(f"Confidence: {source.get('confidence', 0):.2%}")

    output.append("\n" + "-"*60)
    output.append("METADATA")
    output.append("-"*60)
    output.append(f"Confidence Score: {response.get('confidence_score', 0):.2%}")
    
    if response.get("processing_time"):
        output.append(f"Processing Time: {response['processing_time']:.2f}s")
    
    output.append("-"*60 + "\n")
    
    return "\n".join(output)


def main():
    """Main application loop"""
    print_header()

    print("Initializing RAG system...")
    
    if not initialize_rag():
        print("ERROR: Failed to initialize RAG system. Check logs for details.")
        sys.exit(1)
    
    print("RAG system initialized successfully\n")
    pipeline = get_rag_pipeline()
    print_help()

    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            if user_input.startswith("/"):
                if user_input == "/exit":
                    print("\nThank you for using the RAG system. Goodbye!")
                    break
                
                elif user_input == "/help":
                    print_help()
                
                elif user_input == "/status":
                    print_status()
                
                elif user_input == "/clear":
                    import os
                    os.system("clear" if os.name == "posix" else "cls")
                    print_header()
                
                else:
                    print(f"Unknown command: {user_input}")
            
            else:
                print("\nProcessing your question...")
                response = pipeline.process_query(
                    query=user_input,
                    language="en",
                    top_k=3,
                    include_sources=True
                )
                print(format_response(response))
        
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        
        except Exception as e:
            print(f"\nERROR: {str(e)}")
            app_logger.error(f"Application error: {str(e)}")


if __name__ == "__main__":
    main()
import os
import uuid
from app.ingestion.processor import process_document
from app.vectorstore.store_and_query import query_similar_chunks

def main():
    file_path = r"C:\Users\Niyaz\Downloads\Inbred_master_RI_20250614151223.xlsx"


    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    print(f"Processing document: {file_path}")
    
    try:
        # Embed and store
        process_document(file_path)
        print("✅ Embeddings stored in vector DB")

        # Try querying
        test_question = "What is the revenue from Facebook ads?"
        print(f"\nRunning test query: {test_question}")
        results = query_similar_chunks(test_question)

        print("\nTop Results:")
        for i, doc in enumerate(results["documents"][0]):
            print(f"{i+1}. {doc}")
            print(f"   Metadata: {results['metadatas'][0][i]}")
            print(f"   Distance: {results['distances'][0][i]}")
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

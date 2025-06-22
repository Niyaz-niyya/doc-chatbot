from app.vectorstore.store_and_query import add_text_chunks, query_similar_chunks

def test_embedding_storage_and_retrieval():
    # Test data
    test_chunks = [
        "The sky is blue",
        "Grass is green",
        "The sun is bright"
    ]
    
    test_metadata = [
        {"source": "test1", "page": 1},
        {"source": "test2", "page": 1},
        {"source": "test3", "page": 1}
    ]
    
    test_ids = ["1", "2", "3"]

    # Store the test chunks
    print("Adding test chunks to the database...")
    add_text_chunks(test_chunks, test_metadata, test_ids)

    # Test queries
    test_queries = [
        "What color is the sky?",
        "Tell me about the sun"
    ]

    # Perform test queries
    print("\nTesting retrieval:")
    for query in test_queries:
        print(f"\nQuery: {query}")
        results = query_similar_chunks(query, top_k=2)
        
        print("Retrieved documents:")
        for i, doc in enumerate(results['documents'][0]):
            print(f"Document {i + 1}: {doc}")
            print(f"Metadata: {results['metadatas'][0][i]}")
            print(f"Distance: {results['distances'][0][i]}")

if __name__ == "__main__":
    test_embedding_storage_and_retrieval()
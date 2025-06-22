from app.vectorstore.chroma_init import get_chroma_client
from app.embedding.embed_model import embed_text

client = get_chroma_client()
collection = client.get_or_create_collection(name="doc_chunks")

def add_text_chunks(chunks: list[str], metadata: list[dict], ids: list[str]):
    embeddings = embed_text(chunks)
    print(f"Adding {len(chunks)} chunks to the vector store.")
    collection.add(documents=chunks, embeddings=embeddings, metadatas=metadata, ids=ids)

def query_similar_chunks(query: str, top_k: int = 3):
    query_embedding = embed_text([query])[0]
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    return results

def clear_collection():
    all_items = collection.get()  # Get all documents
    if all_items and all_items["ids"]:
        collection.delete(ids=all_items["ids"])

from core.db import DB
from core.ai import SimpleAI

def perform_search(query: str, limit: int = 5):
    # 1. Embed Query
    query_embedding = SimpleAI.embed_text(query)
    
    # 2. Search Chroma
    collection = DB.get_collection()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=limit
    )
    
    # 3. Format Results
    # Chroma returns lists of lists (for batched queries), so we take index 0
    ids = results['ids'][0]
    metadatas = results['metadatas'][0]
    distances = results['distances'][0]
    
    formatted_results = []
    for i, image_id in enumerate(ids):
        formatted_results.append({
            "id": image_id,
            "filename": metadatas[i]['filename'],
            "filepath": metadatas[i]['filepath'],
            "score": 1 - distances[i] if distances else 0 # Cosine Similarity (1 - distance)
        })
        
    return formatted_results

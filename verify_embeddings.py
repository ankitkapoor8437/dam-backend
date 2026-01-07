import sys
import os

# Add the current directory to sys.path so we can import from core/services
sys.path.append(os.getcwd())

from core.db import DB

def verify_chroma():
    print("Initializing DB connection...")
    DB.init_sqlite()
    
    # Use the static method from DB class
    try:
        collection = DB.get_collection()
    except Exception as e:
        print(f"❌ Failed to get collection: {e}")
        return
    
    count = collection.count()
    print(f"Total items in ChromaDB 'images' collection: {count}")
    
    if count > 0:
        print("\nSampling first 5 items...")
        results = collection.peek(limit=5)
        ids = results['ids']
        metadatas = results['metadatas']
        embeddings = results['embeddings']
        
        for i, id_ in enumerate(ids):
            meta = metadatas[i]
            # check embedding length/validity
            emb_len = len(embeddings[i]) if embeddings is not None else 0
            print(f"- ID: {id_}")
            print(f"  Metadata: {meta}")
            print(f"  Embedding Length: {emb_len}")
            
            if emb_len > 0:
                sample_vals = embeddings[i][:3]
                print(f"  Sample Vector: {sample_vals}...")

    # TEST SEARCH CONFUSION MATRIX
    print("\n--- Semantic Confusion Matrix ---")
    from services.search import perform_search
    
    queries = ["city", "car", "cat"]
    for q in queries:
        print(f"\nQuery: '{q}'")
        try:
            results = perform_search(q, limit=3)
            for res in results:
                print(f" - {res['id'][:8]}... (Score: {res['score']:.4f})")
        except Exception as e:
            print(f"❌ Search Failed: {e}")


if __name__ == "__main__":
    verify_chroma()

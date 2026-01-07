import sys
import os
import numpy as np
from PIL import Image
from sentence_transformers import SentenceTransformer, util

# Add path
sys.path.append(os.getcwd())
from core.config import EMBEDDING_MODEL_NAME

def test_similarity():
    # Load model matches core/ai.py
    print(f"Loading {EMBEDDING_MODEL_NAME}...")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    
    # 1. Embed Text
    text = "cat"
    text_emb = model.encode(text, normalize_embeddings=True)
    
    # 2. Embed Image
    img_path = "../test_assets/cat.png"
    if not os.path.exists(img_path):
        print("cat.png not found")
        return
        
    image = Image.open(img_path)
    img_emb = model.encode(image, normalize_embeddings=True)
    
    # 3. Compute Dot Product (Cosine Similarity)
    score = util.dot_score(text_emb, img_emb)[0][0]
    
    print(f"\n--- Results ---")
    print(f"Text: '{text}'")
    print(f"Image: {img_path}")
    print(f"Cosine Similarity: {score:.4f}")

if __name__ == "__main__":
    test_similarity()

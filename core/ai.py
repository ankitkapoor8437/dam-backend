from sentence_transformers import SentenceTransformer
from PIL import Image
from typing import Union, List
from .config import EMBEDDING_MODEL_NAME

class SimpleAI:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            print(f"Loading model {EMBEDDING_MODEL_NAME}...")
            cls._instance = SentenceTransformer(EMBEDDING_MODEL_NAME)
            print("Model loaded.")
        return cls._instance

    @staticmethod
    def embed_text(text: str) -> List[float]:
        model = SimpleAI.get_instance()
        return model.encode(text, normalize_embeddings=True).tolist()

    @staticmethod
    def embed_image(image_path: str) -> List[float]:
        model = SimpleAI.get_instance()
        image = Image.open(image_path)
        return model.encode(image, normalize_embeddings=True).tolist()

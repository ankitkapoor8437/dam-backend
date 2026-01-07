import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
IMAGES_DIR = DATA_DIR / "images"
DB_DIR = DATA_DIR / "db"

# Ensure directories exist
IMAGES_DIR.mkdir(parents=True, exist_ok=True)
DB_DIR.mkdir(parents=True, exist_ok=True)

# Database Config
SQLITE_DB_PATH = DB_DIR / "dam.db"
CHROMA_DB_PATH = DB_DIR / "chroma"

# Model Config
EMBEDDING_MODEL_NAME = "clip-ViT-B-32"

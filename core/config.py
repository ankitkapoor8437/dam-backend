import os
from pathlib import Path

# Base Paths
# Base Paths
# If running in Docker/Cloud, we might want to override DATA_DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# Check for env var, else default to local 'data' folder sibling to 'dam-backend' or inside it
if os.getenv("DATA_DIR"):
    DATA_DIR = Path(os.getenv("DATA_DIR"))
else:
    # Default behavior: try to stay consistent with local setup
    # If file is in ai-dam/dam-backend/core/config.py
    # BASE_DIR is ai-dam/dam-backend
    # We want ai-dam/data ?
    # Let's verify where we are. 
    # For Docker, we will set WORKDIR /app (which is dam-backend content).
    # So we can just use "data" inside it for simplicity or /data volume.
    DATA_DIR = BASE_DIR.parent / "data"

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

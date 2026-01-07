import shutil
import uuid
import os
from fastapi import UploadFile
from core.config import IMAGES_DIR
from core.db import DB
from core.ai import SimpleAI

def process_upload(file: UploadFile):
    # 1. Generate ID and Path
    image_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[1]
    filename = f"{image_id}{ext}"
    file_path = IMAGES_DIR / filename
    
    # 2. Save File
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # 3. Generate Embedding
    embedding = SimpleAI.embed_image(str(file_path))
    
    # 4. Store in SQLite
    conn = DB.get_sqlite_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO images (id, filename, filepath) VALUES (?, ?, ?)",
        (image_id, filename, str(file_path))
    )
    conn.commit()
    conn.close()
    
    # 5. Store in ChromaDB
    collection = DB.get_collection()
    collection.add(
        ids=[image_id],
        embeddings=[embedding],
        metadatas=[{"filename": filename, "filepath": str(file_path)}]
    )
    
    return {"id": image_id, "filename": filename, "status": "indexed"}

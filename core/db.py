import sqlite3
import chromadb
from chromadb.config import Settings
from .config import SQLITE_DB_PATH, CHROMA_DB_PATH

class DB:
    @staticmethod
    def init_sqlite():
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id TEXT PRIMARY KEY,
                filename TEXT,
                filepath TEXT,
                upload_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    @staticmethod
    def get_sqlite_conn():
        return sqlite3.connect(SQLITE_DB_PATH)

    @staticmethod
    def get_chroma_client():
        return chromadb.PersistentClient(path=str(CHROMA_DB_PATH))

    @staticmethod
    def get_collection():
        client = DB.get_chroma_client()
        # Enforce Cosine Similarity for semantic search
        return client.get_or_create_collection(
            name="image_embeddings",
            metadata={"hnsw:space": "cosine"}
        )

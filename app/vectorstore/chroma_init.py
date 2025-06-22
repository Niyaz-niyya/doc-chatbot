import os
import chromadb
from app.config.settings import settings

def get_chroma_client():
    return chromadb.PersistentClient(path=settings.CHROMA_DB_DIR)

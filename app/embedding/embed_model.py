from sentence_transformers import SentenceTransformer
from functools import lru_cache

@lru_cache()
def load_embedding_model():
    model_path = "E:/Adaptnxt/bge-small-en-v1.5"
    return SentenceTransformer(model_path)

def embed_text(texts: list[str]) -> list[list[float]]:
    model = load_embedding_model()
    return model.encode(texts, convert_to_tensor=False).tolist()

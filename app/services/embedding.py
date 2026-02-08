from sentence_transformers import SentenceTransformer
import torch

class EmbeddingService:
    def __init__(self):
        print("Loading SentenceTransformer model...")
        # Using all-MiniLM-L6-v2 as requested (Free & Fast)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Model loaded.")

    def encode(self, texts):
        return self.model.encode(texts, convert_to_tensor=True)

# Singleton instance
embedding_service = EmbeddingService()

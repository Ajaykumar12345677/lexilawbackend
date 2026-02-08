from sentence_transformers import util
from app.services.loader import loader
from app.services.embedding import embedding_service
import torch

class LegalMatcher:
    def __init__(self):
        # Loader loads data at module level, but we ensure it's loaded
        if not loader.combined_data:
            self.data = loader.load_data()
        else:
            self.data = loader.combined_data
            
        self.corpus_embeddings = None
        self._precompute_embeddings()

    def _precompute_embeddings(self):
        print("Pre-computing embeddings for legal corpus...")
        # searching against 'search_text' which combines desc, simpleDesc, etc.
        corpus_texts = [item['search_text'] for item in self.data]
        self.corpus_embeddings = embedding_service.encode(corpus_texts)
        print("Embeddings computed.")

    def search(self, query: str, top_k: int = 3, threshold: float = 0.25):
        # Threshold 0.25 is safer for sentence-transformers which sometimes give lower cosine scores for loose matches.
        # User suggested 0.6 but that might be too strict for cross-domain (plain english -> legal text). 
        # We can adjust.
        
        query_embedding = embedding_service.encode(query)
        cos_scores = util.cos_sim(query_embedding, self.corpus_embeddings)[0]
        
        # Get top k
        top_results = torch.topk(cos_scores, k=min(top_k, len(self.data)))
        
        results = []
        for score, idx in zip(top_results.values, top_results.indices):
            if score < threshold:
                continue
            item = self.data[idx]
            results.append({
                "score": float(score),
                "section": item
            })
            
        return results

matcher = LegalMatcher()

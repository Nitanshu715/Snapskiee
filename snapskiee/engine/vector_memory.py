import numpy as np
from typing import List, Dict, Any

class LocalVectorMemory:
    """
    Lightweight, on-device vector index that enables instant semantic search
    over user scratchpad items without cloud dependencies.
    """

    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.documents: List[Dict[str, Any]] = []
        self.embeddings: List[np.ndarray] = []

    def _mock_embedding(self, text: str) -> np.ndarray:
        """Generates deterministic local embedding representation."""
        # Simple hash-based deterministic normalized vector for mock/prototype
        np.random.seed(abs(hash(text)) % (2**32))
        vec = np.random.randn(self.dimension).astype(np.float32)
        norm = np.linalg.norm(vec)
        return vec / (norm + 1e-9)

    def add_note(self, note_id: str, title: str, content: str, metadata: Dict[str, Any] = None):
        """Indexes a note into local vector memory."""
        embedding = self._mock_embedding(content)
        doc = {
            "id": note_id,
            "title": title,
            "content": content,
            "metadata": metadata or {}
        }
        self.documents.append(doc)
        self.embeddings.append(embedding)

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Semantic search over indexed memories using cosine similarity."""
        if not self.documents:
            return []

        query_vec = self._mock_embedding(query)
        doc_matrix = np.array(self.embeddings)

        # Cosine similarity
        similarities = np.dot(doc_matrix, query_vec)
        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            results.append({
                "score": float(similarities[idx]),
                "document": self.documents[idx]
            })
        return results

from .embeddings import get_simple_embedding


class SimpleVectorStore:
    """
    In-memory vector store for knowledge base embeddings.
    """

    def __init__(self):
        self.vectors = []

    def add_document(self, doc_id: str, text: str, metadata: dict):
        embedding = get_simple_embedding(text)
        self.vectors.append({
            "id": doc_id,
            "text": text,
            "metadata": metadata,
            "embedding": embedding
        })

    def search(self, query: str, top_k: int = 3) -> list:
        query_vec = get_simple_embedding(query)
        scored_docs = []

        for item in self.vectors:
            # Cosine similarity for normalized vectors
            sim = sum(q * d for q, d in zip(query_vec, item["embedding"]))
            scored_docs.append((sim, item))

        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored_docs[:top_k]]


# Global singleton store instance
vector_store_instance = SimpleVectorStore()
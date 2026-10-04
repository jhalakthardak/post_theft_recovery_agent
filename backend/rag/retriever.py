from .document_loader import load_knowledge_base_docs
from .chunker import chunk_text
from .vector_stores import vector_store_instance

_is_indexed = False


def index_knowledge_base():
    """
    Loads knowledge base documents and builds vector store index.
    """
    global _is_indexed
    if _is_indexed:
        return

    raw_docs = load_knowledge_base_docs()
    doc_count = 0

    for doc in raw_docs:
        chunks = chunk_text(doc["content"])
        for idx, chunk in enumerate(chunks):
            doc_id = f"{doc['category']}_{doc['source']}_{idx}"
            metadata = {
                "category": doc["category"],
                "source": doc["source"]
            }
            vector_store_instance.add_document(doc_id, chunk, metadata)
            doc_count += 1

    _is_indexed = True


def retrieve_relevant_guidance(query: str, top_k: int = 3) -> list:
    """
    Retrieves top relevant knowledge base chunks matching the query.
    """
    index_knowledge_base()
    results = vector_store_instance.search(query, top_k=top_k)

    formatted = []
    for item in results:
        formatted.append({
            "category": item["metadata"]["category"],
            "source": item["metadata"]["source"],
            "content": item["text"]
        })

    return formatted
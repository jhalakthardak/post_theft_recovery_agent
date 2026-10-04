def rag_agent(query: str) -> dict:
    """
    Retrieves verified procedural guidance for recovery steps.
    """
    # RAG retriever integration will connect to knowledge base
    return {
        "query": query,
        "procedural_guidance": "Follow official verification steps through authorized government and banking portals."
    }
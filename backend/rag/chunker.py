def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list:
    """
    Splits long documents into manageable text chunks for retrieval.
    """
    words = text.split()
    chunks = []
    
    if len(words) <= chunk_size:
        return [text]

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += (chunk_size - overlap)

    return chunks
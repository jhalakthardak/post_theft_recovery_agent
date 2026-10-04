def get_simple_embedding(text: str) -> list:
    
    """Generates a lightweight vector representation based on term hashing.
    Provides zero-dependency vector compatibility. """
  
    words = text.lower().split()
    vec = [0.0] * 128
    for word in words:
        idx = hash(word) % 128
        vec[idx] += 1.0
    
    # Normalize vector
    
    magnitude = sum(x**2 for x in vec) ** 0.5
    if magnitude > 0:
        vec = [x / magnitude for x in vec]
    
    return vec
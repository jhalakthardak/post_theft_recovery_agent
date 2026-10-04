import os


def load_knowledge_base_docs(kb_root_dir: str = None) -> list:
    """
    Loads text files from the knowledge base directories.
    """
    if not kb_root_dir:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        kb_root_dir = os.path.join(base_dir, "knowledge_base")

    documents = []
    if not os.path.exists(kb_root_dir):
        return documents

    for root, _, files in os.walk(kb_root_dir):
        category = os.path.basename(root)
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read().strip()
                        if content:
                            documents.append({
                                "category": category,
                                "source": file,
                                "content": content
                            })
                except Exception as e:
                    print(f"[DocumentLoader Warning]: Failed to read {file_path}: {e}")

    return documents
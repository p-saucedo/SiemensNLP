def compute_id(text: str, collection_name: str) -> str:
    return f"{collection_name}_{hash(text)}"
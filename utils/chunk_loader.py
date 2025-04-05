import json

def load_chunks(json_path="data/split_chunks.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)
    texts = [c["content"] for c in chunks]
    ids = [c["id"] for c in chunks]
    return texts, ids

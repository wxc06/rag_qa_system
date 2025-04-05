# retrieval/build_index.py
import json
import faiss
import pickle
from embedder import Embedder

def build_faiss_index(json_path='data/split_chunks.json', save_prefix='data/faq_index'):
    with open(json_path, 'r') as f:
        chunks = json.load(f)
    
    embedder = Embedder()
    texts = [c['content'] for c in chunks]
    ids = [c['id'] for c in chunks]

    embeddings = embedder.encode(texts)
    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    faiss.write_index(index, f'{save_prefix}.index')

    with open(f'{save_prefix}_meta.pkl', 'wb') as f:
        pickle.dump({'ids': ids, 'texts': texts}, f)

    print(f"✅ FAISS index built and saved with {len(ids)} entries.")

if __name__ == '__main__':
    build_faiss_index()

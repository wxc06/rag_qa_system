# retrieval/search.py
import faiss
import pickle
from embedder import Embedder

class Retriever:
    def __init__(self, index_path='data/faq_index.index', meta_path='data/faq_index_meta.pkl'):
        self.index = faiss.read_index(index_path)
        with open(meta_path, 'rb') as f:
            meta = pickle.load(f)
        self.ids = meta['ids']
        self.texts = meta['texts']
        self.embedder = Embedder()

    def query(self, question, top_k=3):
        vec = self.embedder.encode([question])
        D, I = self.index.search(vec, top_k)
        results = []
        for i in I[0]:
            results.append(self.texts[i])
        return results

if __name__ == '__main__':
    retriever = Retriever()
    q = input("🧠 Ask a question: ")
    answers = retriever.query(q)
    for idx, ans in enumerate(answers, 1):
        print(f"\n[{idx}] {ans}")

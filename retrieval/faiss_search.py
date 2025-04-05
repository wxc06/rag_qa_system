from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class FaissRetriever:
    def __init__(self, texts, use_approx=True, nlist=100):
        """
        :param texts: list of str, corpus
        :param use_approx: whether to use IndexIVFFlat
        :param nlist: number of clusters for IVFFlat
        """
        self.texts = texts
        self.embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.embeddings = self.embedder.encode(texts, normalize_embeddings=True).astype("float32")
        self.dim = self.embeddings.shape[1]
        self.use_approx = use_approx

        if self.use_approx:
            quantizer = faiss.IndexFlatL2(self.dim)  # 用于初始聚类
            self.index = faiss.IndexIVFFlat(quantizer, self.dim, nlist, faiss.METRIC_L2)
            self.index.train(self.embeddings)  # 先训练聚类中心
        else:
            self.index = faiss.IndexFlatL2(self.dim)

        self.index.add(self.embeddings)

    def search(self, query, top_k=3):
        q_embed = self.embedder.encode([query], normalize_embeddings=True).astype("float32")
        D, I = self.index.search(q_embed, top_k)
        return [self.texts[i] for i in I[0]]

# retrieval/embedder.py
from sentence_transformers import SentenceTransformer
import numpy as np

class Embedder:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts):
        """
        输入一段文本或多个段落，返回嵌入向量（二维数组）
        """
        return self.model.encode(texts, show_progress_bar=False, normalize_embeddings=True)

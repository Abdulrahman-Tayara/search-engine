import os

from sklearn.metrics.pairwise import cosine_similarity

from engine.ir_engine import IREngine
from engine.utils import load_model, load_w2v_model, preprocess, tokenize_content
from gensim.models import Word2Vec
import numpy as np

class Word2VecEngine(IREngine):

    def __init__(self, threshold=0.4, results_limit=None, sort_results_by_similarity=True) -> None:
        self.model = self._load_model()
        self.matrix = self._load_matrix()
        self.documents_ids = self._load_documents_ids()
        self.threshold = threshold
        self.results_limit = results_limit
        self.sort_results_by_similarity = sort_results_by_similarity

    @staticmethod
    def _load_model():
        return load_w2v_model(os.path.join("word2vec", "word2vec.model"))

    @staticmethod
    def _load_matrix():
        return load_model(os.path.join("word2vec", "matrix.pk"))

    @staticmethod
    def _load_documents_ids():
        return load_model(os.path.join("word2vec", "documents_ids.pk"))

    def get_documents_count(self) -> int:
        return len(self.documents_ids)

    def _get_embedding_vector(self, doc_tokens):
        embeddings = []
        size = self.model.vector_size
        if len(doc_tokens) < 1:
            return np.zeros(size)
        else:
            for tok in doc_tokens:
                if tok in self.model.wv.index_to_key:
                    embeddings.append(self.model.wv.get_vector(tok))
                else:
                    embeddings.append(np.random.rand(size))
                    
        return np.mean(embeddings, axis=0)

    def match_query(self, query: str) -> list[tuple[str, float]]:

        query = preprocess(query)

        query_vector = self._get_embedding_vector(tokenize_content(query))

        matched_documents = []

        for i, document_vector in enumerate(self.matrix):
            similarity = cosine_similarity([document_vector], [query_vector])

            if self.threshold is None or similarity >= self.threshold:
                matched_documents.append((self.documents_ids[i], similarity))

        if self.sort_results_by_similarity:
            matched_documents.sort(reverse=True, key=lambda d: d[1])

        if self.results_limit is not None:
            return matched_documents[0: self.results_limit]

        return matched_documents

import os

from sklearn.metrics.pairwise import cosine_similarity

from engine.ir_engine import IREngine
from engine.utils import load_model


class TfIdfEngine(IREngine):

    def __init__(self, threshold=0.000001, results_limit=None, sort_results_by_similarity=True) -> None:
        self.vectorizer = self._load_vectorizer()
        self.matrix = self._load_matrix()
        self.documents_ids = self._load_documents_matrix()
        self.threshold = threshold
        self.results_limit = results_limit
        self.sort_results_by_similarity = sort_results_by_similarity

    @staticmethod
    def _load_vectorizer():
        return load_model(os.path.join("tfidf", "vectorizer.pk"))

    @staticmethod
    def _load_matrix():
        return load_model(os.path.join("tfidf", "matrix.pk")).toarray()

    @staticmethod
    def _load_documents_matrix():
        return load_model(os.path.join("tfidf", "documents_ids.pk"))

    def get_documents_count(self) -> int:
        return len(self.documents_ids)

    def match_query(self, query: str) -> list[tuple[str, float]]:

        query_tfidf = self.vectorizer.transform([query])

        query_vector = query_tfidf.toarray()[0]

        matched_documents = []

        for i, document_vector in enumerate(self.matrix):

            similarity = cosine_similarity(
                [document_vector], [query_vector])[0][0]

            if self.threshold is None or similarity >= self.threshold:
                matched_documents.append((self.documents_ids[i], similarity))

        if self.sort_results_by_similarity:
            matched_documents.sort(reverse=True, key=lambda d: d[1])

        if self.results_limit is not None:
            return matched_documents[0: self.results_limit]

        return matched_documents

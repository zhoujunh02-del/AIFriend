from rank_bm25 import BM25Okapi
from .embedder import get_collection
from collections import defaultdict

class HybridRetriever:
    def __init__(self, collection_name: str, chunks: list[str]):
        self.collection_name = collection_name
        self.chunks = chunks
        self.bm25 = BM25Okapi([chunk.split() for chunk in chunks])

    def vector_search(self, query: str, top_k: int) -> list[str]:
        collection = get_collection(self.collection_name)
        result = collection.query(query_texts=[query], n_results=top_k)
        return result["documents"][0]

    def bm25_search(self, query: str, top_k: int) -> list[str]:
        scores = self.bm25.get_scores(query.split())
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        return [self.chunks[i] for i in top_indices]

    def rrf_merge(self, list1: list[str], list2: list[str], k: int = 60) -> list[str]:
        chunk_score = defaultdict(float)
        for rank, chunk in enumerate(list1):
            chunk_score[chunk] += 1 / (k + rank)
        for rank,chunk in enumerate(list2):
            chunk_score[chunk] += 1 / (k + rank)

        result = sorted(chunk_score.keys(), key= lambda x: chunk_score[x], reverse=True)
        return result

    def retrieve(self, query: str, top_k: int = 5) -> list[str]:
        vector_result = self.vector_search(query, top_k)
        bm25_result = self.bm25_search(query, top_k)
        return self.rrf_merge(vector_result, bm25_result, k = 60)


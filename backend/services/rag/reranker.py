from FlagEmbedding import FlagReranker

class BGEReranker:
    def __init__(self, model_name="BAAI/bge-reranker-base"):
        self.reranker = FlagReranker(model_name)

    def rerank(self, query: str, chunks: list[str], top_k: int) -> list[str]:
        pairs = [[query, chunk] for chunk in chunks]
        scores = self.reranker.compute_score(pairs)

        sorted_pairs = sorted(zip(chunks, scores), key=lambda x:x[1], reverse=True)
        sorted_chunks = [chunk for chunk,score in sorted_pairs]
        return sorted_chunks[:top_k]
    
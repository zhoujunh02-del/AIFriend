from .retriever import HybridRetriever
from .reranker import BGEReranker
from services.agent.agent import run_agent

def rag_query(persona_prompt, query, retriever, reranker, top_k = 3):
    top_5_chunks = retriever.retrieve(query, top_k = 5)
    top_3_chunks = reranker.rerank(query, top_5_chunks, top_k=top_k)
    return top_3_chunks
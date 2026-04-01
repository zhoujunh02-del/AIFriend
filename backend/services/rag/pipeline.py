from anthropic import Anthropic
from .retriever import HybridRetriever
from .reranker import BGEReranker

client = Anthropic()

def build_system_prompt(persona_prompt: str, chunks: list[str]) -> str:
    if not chunks:
        return persona_prompt
    
    context = "\n".join(chunks)
    return f"{persona_prompt}\n\nThe following is relevant background knowledge, please refer to it when answering:\n---\n{context}\n---"


def rag_query(persona_prompt, query, retriever, reranker, top_k = 3):
    top_5_chunks = retriever.retrieve(query, top_k = 5)
    top_3_chunks = reranker.rerank(query, top_5_chunks, top_k = 3)
    system_prompt = build_system_prompt(persona_prompt, top_3_chunks)

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role" : "user", "content" : query}]
        )
    return response.content[0].text
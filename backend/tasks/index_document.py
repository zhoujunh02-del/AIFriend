from celery import shared_task
from django.utils import timezone
from apps.knowledge.models import KnowledgeDocument
from services.rag.parser import parse_document
from services.rag.chunker import chunk_text
from services.rag.embedder import add_chunks

@shared_task
def index_document(document_id: str):
    document = KnowledgeDocument.objects.get(id=document_id)

    try:
        text = parse_document(document.file_path)
        chunks = chunk_text(text)
        add_chunks(document.knowledge_base.collection_name, chunks)

    except Exception as e:
        document.status = "failed"
        document.error_message = str(e)
        document.save()
        return
    
    document.status = "indexed"
    document.chunk_count = len(chunks)
    document.indexed_at = timezone.now()
    document.save()

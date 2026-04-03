from apps.chat.models import ChatSession, Message
from langchain_anthropic import ChatAnthropic
from django.db.models import Sum

def count_tokens(text):
    return max(1, len(text) // 4)


def get_session_tokens(session):
    result = session.messages.aggregate(total=Sum('token_count'))
    return result['total'] or 0

def should_compress(session, threshold=3000):
    return get_session_tokens(session) > threshold

def compress(session):
    messages = list(session.messages.order_by('created_at'))
    if not messages:
        return

    history_text = "\n".join(
        f"{msg.role}: {msg.content}" for msg in messages
    )

    llm = ChatAnthropic(model="claude-haiku-4-5-20251001")
    summary = llm.invoke(
        f"Please summarize this conversation concisely:\n\n{history_text}"
    ).content

    session.memory_summary = summary
    session.save(update_fields=['memory_summary'])

    session.messages.all().delete()

def assemble_context(session):
    history =[]

    if session.memory_summary:
        history.append(("human", "Here is a summary of our conversation so far."))
        history.append(("ai", session.memory_summary))
    
    for msg in session.messages.order_by('created_at'):
        role = "human" if msg.role == "user" else "ai"
        history.append((role, msg.content))

    return history

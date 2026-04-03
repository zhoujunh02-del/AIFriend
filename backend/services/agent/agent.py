from langchain_anthropic import ChatAnthropic
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from .tools import get_current_datetime, calculator, web_search, get_weather

def build_system_prompt(persona_prompt: str, chunks: list[str]) -> str:
    if not chunks:
        return persona_prompt
    
    context = "\n".join(chunks)
    return f"{persona_prompt}\n\nThe following is relevant background knowledge, please refer to it when answering:\n---\n{context}\n---"


def run_agent(persona_prompt, query, rag_context, on_token=None):
    callbacks = []
    if on_token:
        from .streaming import StreamingCallbackHandler
        callbacks = [StreamingCallbackHandler(on_token)]

    llm = ChatAnthropic(
        model="claude-haiku-4-5-20251001",
        streaming=True,
        callbacks=callbacks
        )
        
    tools = [get_current_datetime, calculator, web_search, get_weather]

    system_prompt = build_system_prompt(persona_prompt, rag_context)

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, return_intermediate_steps=True)

    result = executor.invoke({"input": query})

    logs = [
        {
            "tool": action.tool,
            "input": action.tool_input,
            "output": output,
        }
        for action, output in result["intermediate_steps"]
    ]

    return {"answer": result["output"], "function_call_log": logs}

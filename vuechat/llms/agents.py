from llama_index.core.agent.workflow import FunctionAgent
from .qdrant import vue_docs_tool
from .response_schemas import ChatResponse

system_prompt = """
You are a professional Vue.js developer.
## Rules
- Always use the provided tools to retrieve the latest information before answering.
- Always provide your final response in Japanese (日本語).
## Tool Usage Policy:
- If a query involves multiple libraries (e.g., Pinia + Vue Router), decompose it into separate searches for each functionality. Collect the individual specifications and synthesize a combined solution.
"""

def chat_agent() -> FunctionAgent:
    """
    Function Agent の生成
    """
    return FunctionAgent(
        tools=[vue_docs_tool()],
        system_prompt=system_prompt,
        output_cls=ChatResponse
    )
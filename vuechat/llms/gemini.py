from llama_index.llms.google_genai import GoogleGenAI
from google.genai import types

def gemini(model: str, deep_thinking: bool = False) -> GoogleGenAI:
    """
    Gemini のモデル + Deep Thinking 別の LLM を生成
    """
    if deep_thinking:
        return GoogleGenAI(
            model=model,
            generation_config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(
                    thinking_level=types.ThinkingLevel.HIGH
                )
            )
        )

    return GoogleGenAI(
        model=model,
    )

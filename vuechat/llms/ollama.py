from llama_index.embeddings.ollama import OllamaEmbedding

model = OllamaEmbedding(model_name="qwen3-embedding")

def ollama_embedding() -> OllamaEmbedding:
    """
    OllamaEmbedding クライアントを返す。
    """
    return model

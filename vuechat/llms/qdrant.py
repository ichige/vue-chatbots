from qdrant_client import QdrantClient
from llama_index.core import VectorStoreIndex
from llama_index.core.tools import (
    QueryEngineTool,
    ToolMetadata
)
from llama_index.vector_stores.qdrant import QdrantVectorStore
from .ollama import ollama_embedding
from .query_engine import VueDocQueryEngine

def qdrant_client() -> QdrantClient:
    """
    Qdrant 非同期クライアント
    """
    return QdrantClient(
        host="127.0.0.1"
    )

def vue_docs_tool() -> QueryEngineTool:
    """
    Vue Document tool
    """
    index = VectorStoreIndex.from_vector_store(
        vector_store=QdrantVectorStore(
            collection_name="vue_docs",
            client=qdrant_client(),
        ),
        embed_model=ollama_embedding(),
    )

    return QueryEngineTool(
        query_engine=VueDocQueryEngine(
            retriever=index.as_retriever(similarity_top_k=3)
        ),
        metadata=ToolMetadata(
            name="search_vue_documents",
            description="""
Provides access to the latest documentation for Vue.js, Vue Router, and Pinia. 
Queries must be in English.
            """
        ),
    )




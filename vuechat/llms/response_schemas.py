from pydantic import (
    BaseModel,
    Field
)
from typing import (
    Literal
)

class VueDocument(BaseModel):
    """
    Structured Vue.js document
    """
    score: float = Field(
        description="Relevance score from 0.0 to 1.0. Higher is more relevant."
    )
    text: str = Field(
        description="The document content. Contains Markdown, source code, and technical details."
    )
    doc_type: Literal["vue", "router", "pinia"] = Field(
        description="The target library. Identifies which API or framework the text belongs to."
    )
    doc_version: str = Field(
        description="The library version this document covers. e.g., '>=3.x', '>=4.x'."
    )
    doc_category: Literal["guide", "reference", "example"] = Field(
        description="The purpose of the content. 'guide' for concepts, 'reference' for API specs, 'example' for implementation."
    )
    doc_url: str = Field(
        description="The official documentation source URL."
    )

class VueDocResponse(BaseModel):
    """
    Structured list of Vue.js documentation results used to generate accurate code and explanations.
    """
    contents: list[VueDocument] = Field(
        description="A list of relevant document segments found in the knowledge base."
    )

class ChatResponse(BaseModel):
    """
    Final output schema for chat response.
    """
    text: str = Field(description="The answer text.")
    doc_urls: list[str] = Field(description="List of URLs extracted directly from the tool output.", default=[])

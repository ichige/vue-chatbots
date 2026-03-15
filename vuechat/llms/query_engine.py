from llama_index.core.query_engine import CustomQueryEngine
from llama_index.core.retrievers import BaseRetriever
from llama_index.core.postprocessor import SimilarityPostprocessor
from .response_schemas import (
    VueDocument,
    VueDocResponse
)

class VueDocQueryEngine(CustomQueryEngine):
    """
    Vue Document Query Engine
    """
    retriever: BaseRetriever
    def custom_query(self, query: str, ) -> VueDocResponse:
        """
        カスタムクエリで任意のデータ構造を返す。
        """
        # Similarity(類似度)でフィルタするプロセッサ
        processor = SimilarityPostprocessor(similarity_cutoff=0.0)
        print(f"query: {query}")
        nodes = self.retriever.retrieve(query)
        print(f"nodes: {len(nodes)}")
        # フィルタリング(スコア基準)
        filtered = processor.postprocess_nodes(nodes)
        print(f"filtered: {len(filtered)}")

        # VueDocument へ変換
        contents: list[VueDocument] = []
        for i, node in enumerate(filtered):
            print(f"score: {node.score}, file_name: {node.metadata.get("file_name")}, document_title: {node.metadata.get("document_title")}")
            contents.append(VueDocument(
                score=node.score,
                text=node.text,
                doc_type=node.metadata.get("doc_type", "unknown"),
                doc_category=node.metadata.get("doc_category", "unknown"),
                doc_version=node.metadata.get("doc_version", "unknown"),
                doc_url=node.metadata.get("doc_url", "unknown"),
            ))

        return VueDocResponse(contents=contents)
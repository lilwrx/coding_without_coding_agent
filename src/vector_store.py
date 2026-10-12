from typing import List

from fastembed import TextEmbedding
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http import models


class FastEmbedAdapter(Embeddings):
    """Expose FastEmbed through the LangChain embeddings interface."""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = TextEmbedding(model_name=model_name)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [vector.tolist() for vector in self.model.embed(texts)]

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]


class VectorStoreManager:
    def __init__(
        self,
        qdrant_url: str,
        collection_name: str,
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        self.qdrant_url = qdrant_url
        self.collection_name = collection_name
        self.embedding = FastEmbedAdapter(embedding_model)
        self.client = QdrantClient(url=self.qdrant_url)
        self.vector_size = len(self.embedding.embed_query("vector dimension check"))

    def init_collection(self) -> None:
        collections = {
            collection.name
            for collection in self.client.get_collections().collections
        }
        if self.collection_name in collections:
            info = self.client.get_collection(self.collection_name)
            vectors_config = info.config.params.vectors
            if isinstance(vectors_config, dict):
                raise ValueError(
                    f"Collection '{self.collection_name}' đang dùng cấu hình nhiều vector; "
                    "hãy chọn tên collection mới cho embedding local."
                )
            if vectors_config.size != self.vector_size:
                raise ValueError(
                    f"Collection '{self.collection_name}' có vector size "
                    f"{vectors_config.size}, nhưng model local cần {self.vector_size}. "
                    "Hãy chọn collection mới hoặc xóa collection cũ nếu không cần dữ liệu trong đó."
                )
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(
                size=self.vector_size,
                distance=models.Distance.COSINE,
            ),
        )

    def add_documents(self, chunks: List[Document]) -> None:
        if not chunks:
            return
        self.init_collection()
        vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name,
            embedding=self.embedding,
        )
        vector_store.add_documents(chunks)

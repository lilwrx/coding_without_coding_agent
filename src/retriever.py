from src.vector_store import VectorStoreManager

from langchain_qdrant import QdrantVectorStore
from langchain_core.documents import Document

from typing import List, Tuple

class DocumentRetriever:
    def __init__(self,vector_store_manager: VectorStoreManager):
        self.manager=vector_store_manager

        if not self.manager.client.collection_exists():
            raise ValueError(
                f"Không tìm thấy collection: {self.manager.collection_name}"
            )

        self.vector_store = QdrantVectorStore(
            client=self.manager.client,
            collection_name=self.manager.collection_name,
            embedding=self.manager.embedding,
        )

    def search (self, query:str,k:int =5)-> List[Tuple[Document,float]]:
        if not query or not query.strip():
            raise ValueError("Cau hoi khong duoc de trong")
        
        if k<=0:
            raise ValueError("k phai lon hon 0")
        
        return self.vector_store.similarity_search_with_score(
            query=query.strip(),
            k=k,
        )
        


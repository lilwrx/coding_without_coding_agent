import os
from typing import List
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.http import models

class VectorStoreManager :
    def __init__ (self,qdrant_url:str,collection_name:str):
        self.qdrant_url=qdrant_url
        self.collection_name=collection_name
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.client=QdrantClient(url=self.qdrant_url)
    def init_collection (self,vector_size:int =1536):
        collections = [c.name for c in self.client.get_collections().collections]
        if self.collection_name not in collections:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=vector_size,  # 1536 là chiều rộng vector của text-embedding-3-small
                    distance=models.Distance.COSINE
                )
            )
            print(f"🚀 Đã tạo mới collection '{self.collection_name}' trên Qdrant.")
    def add_documents(self, chunks: List[Document]):
        self.init_collection()
        
        vector_store = Qdrant(
            client=self.client,
            collection_name=self.collection_name,
            embeddings=self.embeddings
        )
        vector_store.add_documents(chunks)
        print(f"💾 Đã lưu thành công {len(chunks)} chunks vào Vector DB!")
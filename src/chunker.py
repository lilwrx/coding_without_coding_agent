from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

class TextChunker:
    def __init__ (self, chunk_size: int =500 , chunk_overlap: int =50):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n","\n","."," ",""],
            keep_separator=True
        )
    def split_documents(self, documents: List[Document]) -> List[Document]:
        chunks = self.splitter.split_documents(documents)
        print(f"✂️ Đã chia thành {len(chunks)} chunks (size={self.splitter._chunk_size}, overlap={self.splitter._chunk_overlap}).")
        return chunks

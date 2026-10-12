import os
from typing import List 
from langchain_community.document_loaders import PyPDFLoader , TextLoader , Docx2txtLoader
from langchain_core.documents import Document

class DocumentLoader :
    @staticmethod
    def load_document(file_path: str) -> List[Document]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Không tìm thấy file: {file_path}")
        ext=os.path.splitext(file_path)[-1].lower()
        if ext==".pdf":
            loader=PyPDFLoader(file_path)
        elif ext==".docx":
            loader=Docx2txtLoader(file_path)
        elif ext in [".txt",".md"]:
            loader=TextLoader(file_path,encoding="utf-8")
        else :
            raise ValueError(f"Định dạng không {ext} chưa được hỗ trợ")
        docs= loader.load()
        print(f"Da tai thanh cong {len(docs)} trang/phan tu file: {file_path}")
        return docs

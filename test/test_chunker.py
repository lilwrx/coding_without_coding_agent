from src.chunker import TextChunker
from langchain_core.documents import Document
import pytest

@pytest.fixture 
def sample_documents():
    doc1=Document(
        page_content="Đây là đoạn văn ngắn thứ nhất. Nó dùng để test chunking cơ bản.",
        metadata={"source": "doc1.txt", "page": 1}
    )
    long_text="Bài văn mẫu dài"*30
    doc2=Document(
        page_content=long_text,
        metadata={"source":"doc2.txt","page":2}
    )
    return [doc1,doc2]

def test_chunker_initialization():
    chunker = TextChunker(chunk_size=200, chunk_overlap=20)
    assert chunker.splitter._chunk_size == 200
    assert chunker.splitter._chunk_overlap == 20

def test_split_documents_output_type(sample_documents):
    chunker= TextChunker(chunk_size=100,chunk_overlap=20)
    chunks= chunker.split_documents(sample_documents)

    assert isinstance(chunks,list)
    assert len (chunks)>0
    assert all(isinstance(chunk,Document)for chunk in chunks)

def test_chunk_size_limit(sample_documents):
    max_size =100
    chunker =TextChunker(chunk_size=max_size,chunk_overlap=10)
    chunks= chunker.split_documents(sample_documents)

    for chunk in chunks:
        assert len(chunk.page_content)<=max_size

def test_metadata_preservition(sample_documents):
    chunker=TextChunker(chunk_size =100 ,chunk_overlap=20)
    chunks = chunker.split_documents(sample_documents)

    doc1_chunks=[c for c in chunks if c.metadata.get("source")=="doc1.txt"]
    assert len(doc1_chunks)>0
    assert doc1_chunks[0].metadata["page"] == 1

def test_empty_document_list():
    chunker = TextChunker()
    chunks =chunker.split_documents([])
    assert chunks ==[]
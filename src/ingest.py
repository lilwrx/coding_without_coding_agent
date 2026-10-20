# src/ingest.py
import logging
import time
from pathlib import Path

from src.chunker import TextChunker
from src.loader import DocumentLoader
from src.vector_store import VectorStoreManager

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


def ingest_file(
    file_path: Path,
    vector_store: VectorStoreManager,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> int:
    """Đọc, chia nhỏ và lưu một file; trả về số chunks đã xử lý."""
    start = time.perf_counter()
    logger.info("Bắt đầu xử lý: %s", file_path.name)

    documents = DocumentLoader.load_document(str(file_path))
    logger.info("Đã tải %d phần tài liệu", len(documents))

    chunker = TextChunker(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    chunks = chunker.split_documents(documents)
    logger.info("Đã tạo %d chunks", len(chunks))

    if chunks:
        vector_store.add_documents(chunks)
        logger.info("Đã gửi %d chunks lên Qdrant", len(chunks))
    else:
        logger.warning("Không có nội dung để lưu: %s", file_path.name)

    elapsed = time.perf_counter() - start
    logger.info("Hoàn tất %s trong %.2f giây", file_path.name, elapsed)
    return len(chunks)

# src/ingest.py

import argparse
import logging
import os
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


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Nạp file trong thư mục data vào Qdrant."
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data"),
        help="Thư mục chứa PDF, DOCX, TXT hoặc MD (mặc định: data/).",
    )
    parser.add_argument(
        "--qdrant-url",
        default=os.getenv("QDRANT_URL", "http://localhost:6333"),
        help="Địa chỉ Qdrant.",
    )
    parser.add_argument(
        "--collection",
        default=os.getenv("COLLECTION_NAME", "documents"),
        help="Tên collection Qdrant.",
    )
    parser.add_argument(
        "--embedding-model",
        default=os.getenv(
            "FASTEMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
        ),
        help="Tên model FastEmbed chạy local.",
    )
    args = parser.parse_args()

    if not args.data_dir.is_dir():
        parser.error(f"Không tìm thấy thư mục dữ liệu: {args.data_dir}")

    supported_extensions = {".pdf", ".docx", ".txt", ".md"}
    files = sorted(
        path
        for path in args.data_dir.iterdir()
        if path.is_file() and path.suffix.lower() in supported_extensions
    )

    if not files:
        logger.warning("Không tìm thấy file được hỗ trợ trong %s", args.data_dir)
        return

    vector_store = VectorStoreManager(
        qdrant_url=args.qdrant_url,
        collection_name=args.collection,
        embedding_model=args.embedding_model,
    )

    pipeline_start = time.perf_counter()
    total_chunks = 0
    failed_files = []

    for file_path in files:
        try:
            total_chunks += ingest_file(file_path, vector_store)
        except Exception:
            logger.exception("Lỗi khi xử lý %s", file_path.name)
            failed_files.append(file_path.name)

    elapsed = time.perf_counter() - pipeline_start
    logger.info(
        "Pipeline hoàn tất: %d file, %d chunks, %.2f giây",
        len(files),
        total_chunks,
        elapsed,
    )

    if failed_files:
        logger.error("Các file xử lý thất bại: %s", ", ".join(failed_files))


if __name__ == "__main__":
    main()

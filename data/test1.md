# Hướng dẫn Cấu hình Hệ thống Ingest Dữ liệu

Tài liệu này mô tả chi tiết quy trình thiết lập và vận hành luồng ingest (nhập liệu) tự động cho hệ thống cơ sở tri thức doanh nghiệp.

## 1. Tổng quan kiến trúc
Luồng ingest chịu trách nhiệm tiếp nhận tài liệu thô từ nhiều nguồn khác nhau (Markdown, PDF, TXT), thực hiện tiền xử lý, chia nhỏ văn bản (chunking) và lưu trữ vào Vector Database.

### Các thành phần chính:
- **Connector Service**: Thu thập tài liệu từ kho lưu trữ (Git, S3, Local).
- **Parser Engine**: Phân tích cú pháp, trích xuất siêu dữ liệu (metadata) và tiêu đề.
- **Embedding Model**: Chuyển đổi các đoạn văn bản (chunks) thành các vector số học.

---

## 2. Các bước cấu hình chi tiết

### Bước 1: Thiết lập tham số Chunking
Để tối ưu hóa độ chính xác khi truy xuất thông tin (RAG), kích thước chunk cần được cấu hình phù hợp với loại tài liệu:

```json
{
  "chunk_size": 512,
  "chunk_overlap": 64,
  "separators": ["\n\n", "\n", " ", ""]
}
```

### Bước 2: Kết nối Vector Database
Hỗ trợ các cơ sở dữ liệu vector phổ biến như Qdrant, Milvus và Pinecone. Ví dụ cấu hình kết nối Qdrant:

```yaml
vector_db:
  provider: "qdrant"
  host: "localhost"
  port: 6333
  collection_name: "enterprise_knowledge"
  distance_metric: "Cosine"
```

---

## 3. Xử lý lỗi thường gặp
- **Lỗi tràn bộ nhớ (OOM)**: Thường xảy ra khi file đầu vào quá lớn. *Giải pháp*: Giảm `batch_size` xuống mức 16 hoặc 32.
- **Mất mát siêu dữ liệu**: Kiểm tra lại định dạng YAML front-matter ở đầu mỗi file Markdown.
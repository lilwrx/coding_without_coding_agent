# 📋 WEEK 1: Data Ingestion & Vector Indexing Pipeline

> **Mục tiêu tuần 1:** Dựng hoàn chỉnh một pipeline đọc tài liệu đa định dạng, cắt nhỏ văn bản (Chunking), tạo Embeddings và lưu trữ vào Vector Database kèm Metadata đầy đủ.

---

## 📅 Danh sách Task Chi tiết Theo Ngày

### 🟢 Ngày 1: Cấu hình Môi trường & Hạ tầng Vector DB
- [*] Khởi tạo thư mục dự án chuẩn theo cấu trúc phân tách rõ ràng (`data/`, `src/`, `tests/`).
- [*] Tạo môi trường ảo Python (`python -m venv venv`) và activate môi trường.
- [*] Viết file `docker-compose.yml` để khởi chạy **Qdrant Vector DB** trên Docker.
- [*] Tạo file `.env` chứa các biến môi trường (`OPENAI_API_KEY`, `QDRANT_URL`, `COLLECTION_NAME`).
- [*] Viết file `requirements.txt` với các thư viện cốt lõi: `pypdf`, `python-docx`, `langchain-text-splitters`, `langchain-openai`, `qdrant-client`, `python-dotenv`.
- [*] *Checkpoints:* Kiểm tra Docker container Qdrant chạy thành công và truy cập được Dashboard tại `http://localhost:6333/dashboard`.

---

### 🟢 Ngày 2: Viết Document Loaders Module (`src/loader.py`)
- [*] Viết class `DocumentLoader` xử lý đọc nhiều định dạng file đầu vào: `.pdf`, `.docx`, `.txt`, `.md`.
- [*] Sử dụng các parser chuẩn: `PyPDFLoader` (cho PDF), `Docx2txtLoader` (cho Word), `TextLoader` (cho văn bản thuần).
- [*] Thêm xử lý ngoại lệ (Exception Handling): File không tồn tại, file bị khóa mật khẩu, định dạng file không hỗ trợ.
- [*] Thêm tính năng tự động trích xuất thông tin cơ bản: Tên file (`source`), Số trang (`page`), Ngày nạp (`created_at`).
- [*] *Checkpoints:* Chạy unit test/script nhỏ đọc thành công file PDF/Word mẫu và in ra số trang + metadata.

---

### 🟢 Ngày 3: Thiết lập Chunking Strategy (`src/chunker.py`)
- [*] Tích hợp `RecursiveCharacterTextSplitter` với thứ tự chia nhỏ ưu tiên: `["\n\n", "\n", ".", " ", ""]`.
- [*] Thử nghiệm và thiết lập bộ thông số mặc định:
  - `chunk_size = 500` (tokens/characters)
  - `chunk_overlap = 50` (tokens/characters để giữ ngữ cảnh)
- [*] Bổ sung Metadata riêng cho từng chunk: `chunk_id`, `chunk_index` (vị trí đoạn văn trong file).
- [*] *Checkpoints:* Kiểm tra đầu ra của chunker đảm bảo không bị mất văn bản giữa các đoạn và gãy câu vô lý.

---

### 🟢 Ngày 4: Embedding & Vector DB Manager (`src/vector_store.py`)
- [*] Tích hợp client `OpenAIEmbeddings` với model `text-embedding-3-small` (1536 dims).
- [*] Viết class `VectorStoreManager` kết nối với Qdrant Client SDK.
- [*] Viết hàm tự động khởi tạo Collection trên Qdrant nếu chưa tồn tại (Distance Metric = `COSINE`).
- [*] Viết hàm `add_documents` để tạo embeddings từ danh sách chunks và lưu trữ trực tiếp vào Qdrant.
- [*] *Checkpoints:* Mở Qdrant Dashboard xem các vector points đã được đẩy vào Collection cùng đủ thuộc tính Payload (Metadata).

---

### 🟢 Ngày 5: Đóng gói Pipeline & Testing (`ingest.py`)
- [ ] Tạo file script `ingest.py` ở thư mục gốc kết nối toàn bộ 3 bước: `Loader` ➔ `Chunker` ➔ `VectorStore`.
- [ ] Thêm log thông báo chi tiết thời gian chạy và số lượng chunks được lưu ở từng giai đoạn.
- [ ] Bỏ 2-3 tài liệu thực tế (PDF báo cáo, file Word) vào thư mục `data/` và chạy thử toàn bộ luồng.
- [ ] *Checkpoints:* Ingestion pipeline chạy mượt mà từ đầu đến cuối không tạo lỗi, dữ liệu xuất hiện đầy đủ trên Qdrant.

---

## 🚀 Các hướng Scale chuyên nghiệp cho Tuần 1 (Nếu hoàn thành sớm)

Nếu bạn làm xong sớm 5 ngày trên, hãy nâng cấp pipeline Ingestion lên chuẩn **Enterprise-Grade** theo các hướng sau:

### 1. Scale về Khả năng xử lý Văn bản Phức tạp (Document Intelligence)
* **Table & Image OCR:** Với file PDF chứa bảng biểu hoặc ảnh scanned, `PyPDF` thường bị mất dữ liệu. Scale bằng cách tích hợp **Unstructured** hoặc **LLM Vision (GPT-4o)** để parse các bảng (Tables) thành dạng Markdown trước khi chunking.
* **Semantic Chunking:** Thay vì cắt theo ký tự cố định (`RecursiveSplitter`), chuyển sang dùng **Semantic Chunker** (dựa trên khoảng cách Cosine giữa các câu) để nhóm các câu có cùng ý nghĩa vào chung một chunk.
* **Parent-Child / Hierarchical Chunking:** Lưu các **Small Chunks** (~150 tokens) để tìm kiếm độ chính xác cao, nhưng gán kèm tham chiếu đến **Parent Chunk** lớn hơn (~800 tokens) để khi truyền cho LLM có đầy đủ bối cảnh rộng.

### 2. Scale về Hiệu năng Ingestion (High-Throughput)
* **Async & Batch Ingestion:** Chuyển đổi các hàm embedding & upload sang xử lý bất đồng bộ (`asyncio`) và gửi dữ liệu theo Batch (ví dụ: 100 chunks/batch) để giảm thời gian chờ Network I/O.
* **Multiprocessing / Parallel Processing:** Nếu cần nạp hàng nghìn file PDF cùng lúc, sử dụng `ProcessPoolExecutor` của Python để chia file cho nhiều CPU Core xử lý song song.

### 3. Scale về Quản lý Dữ liệu & Metadata (Data Governance)
* **Deduplication (Chống trùng lặp dữ liệu):** Tính MD5/SHA256 Hash của file hoặc nội dung chunk trước khi embed. Nếu file/chunk đã tồn tại trong Vector DB thì bỏ qua, tránh tốn tiền API OpenAI và tốn bộ nhớ.
* **Document-Level Security (RBAC Metadata):** Bổ sung thuộc tính phân quyền vào Payload của từng chunk: `allowed_roles: ["admin", "hr_team"]`. Giúp mở đường cho tính năng phân quyền ở các tuần sau.
* **Change Data Capture (CDC / Sync):** Thêm trường `file_checksum` để khi người dùng cập nhật file mới, hệ thống tự biết xóa các chunk cũ trong Qdrant và thay bằng các chunk mới.

---

## 🧪 Checklist Đánh giá Hoàn thành Tuần 1 (Definition of Done)
- [ ] Chạy `python ingest.py` thành công không lỗi.
- [ ] Kiểm tra Qdrant Dashboard thấy Collection có chứa các Vector Points.
- [ ] Mỗi Vector Point lưu trữ đủ thông tin văn bản gốc (`page_content`) và các trường Metadata (`source`, `page`, `chunk_id`).
- [ ] Mã nguồn được commit sạch sẽ lên Git với file `.gitignore` đã chặn file `.env` và virtualenv.
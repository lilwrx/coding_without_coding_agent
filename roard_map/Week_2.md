# WEEK 2: Retrieval & RAG Question Answering

> **Mục tiêu tuần 2:** Xây dựng luồng hỏi đáp trên dữ liệu đã nạp: nhận câu hỏi, tìm các đoạn liên quan trong Qdrant, đưa đoạn trích làm ngữ cảnh và trả lời có dẫn nguồn. Ưu tiên làm retrieval chạy ổn định trước; phần sinh câu trả lời phải có thể cấu hình riêng với phần embedding local.

---

## Danh sách task theo ngày

### Ngày 1: Tạo tầng truy vấn (`src/retriever.py`)

- [ ] Tạo class `DocumentRetriever` nhận `VectorStoreManager` hoặc Qdrant vector store đã cấu hình.
- [ ] Viết hàm `search(query, k=5)` để tìm top-k chunks liên quan trong collection.
- [ ] Tái sử dụng đúng embedding model local đã dùng khi ingest; không tạo collection hoặc model khác cho luồng truy vấn.
- [ ] Kiểm tra query rỗng, `k <= 0`, collection chưa tồn tại và collection chưa có point; trả lỗi/thông báo dễ hiểu.
- [ ] Trả kết quả có `page_content`, metadata nguồn và điểm liên quan nếu backend cung cấp.
- [ ] **Checkpoint:** Một câu hỏi thử trả về danh sách chunks có nội dung và metadata lấy từ Qdrant.

### Ngày 2: Bộ lọc metadata và định dạng nguồn

- [ ] Cho phép lọc kết quả theo `source` hoặc metadata khác mà loader/chunker đang lưu.
- [ ] Xác định định dạng metadata thống nhất giữa loader, chunker và Qdrant: tên file, trang, chunk index/id.
- [ ] Viết hàm định dạng kết quả thành các mục dễ đọc, ví dụ `[1] test1.md, trang 1` kèm nội dung trích dẫn.
- [ ] Không tự bịa nguồn khi metadata thiếu; hiển thị rõ `không rõ nguồn`.
- [ ] **Checkpoint:** Có thể truy vấn toàn bộ collection hoặc lọc theo một file, và nhìn thấy nguồn của từng đoạn.

### Ngày 3: Đánh giá retrieval và viết test

- [ ] Tạo bộ câu hỏi kiểm thử nhỏ (5–10 câu) mà câu trả lời có trong hai file Markdown hiện tại.
- [ ] Viết test cho kết quả top-k, lọc theo nguồn, query rỗng và collection rỗng.
- [ ] Mock Qdrant/embeddings trong unit test để test không cần mạng, OpenAI API hay Qdrant đang chạy.
- [ ] Chạy thêm một lượt integration test thủ công với Qdrant local; ghi lại câu hỏi, nguồn trả về và nhận xét đúng/sai.
- [ ] Điều chỉnh `chunk_size`, `chunk_overlap` hoặc `k` nếu kết quả hay cắt mất ngữ cảnh.
- [ ] **Checkpoint:** Bộ test retrieval chạy ổn định; phần lớn câu hỏi thử trả về đúng tài liệu nguồn trong top-k.

### Ngày 4: Tạo prompt và câu trả lời có căn cứ (`src/qa.py`)

- [ ] Viết hàm ghép câu hỏi với các chunks đã truy hồi thành context có nhãn nguồn.
- [ ] Viết prompt yêu cầu model chỉ trả lời dựa trên context; nếu context không đủ thì nói rõ chưa tìm thấy thông tin.
- [ ] Yêu cầu câu trả lời gắn ký hiệu nguồn như `[1]`, `[2]`, tương ứng chính xác với chunks được đưa vào prompt.
- [ ] Chọn chat model qua cấu hình môi trường; không hard-code API key trong source code.
- [ ] Xử lý riêng lỗi thiếu API key, hết quota, lỗi mạng và trường hợp không tìm thấy chunks.
- [ ] **Checkpoint:** Với một câu hỏi có đáp án trong tài liệu, câu trả lời nêu đúng thông tin và chỉ dẫn về nguồn tương ứng.

### Ngày 5: Đóng gói lệnh hỏi đáp và kiểm tra end-to-end

- [ ] Tạo script `src/query.py` hoặc CLI để nhập câu hỏi từ tham số dòng lệnh.
- [ ] Cho phép cấu hình `QDRANT_URL`, `COLLECTION_NAME`, `TOP_K` và model trả lời qua `.env` hoặc tham số CLI.
- [ ] In câu trả lời, danh sách nguồn và thời gian retrieval/generation; không in API key hay toàn bộ biến môi trường.
- [ ] Thử câu hỏi có đáp án, câu hỏi không có trong tài liệu và collection rỗng.
- [ ] Cập nhật hướng dẫn chạy trong `README.md`, bao gồm cách nạp tài liệu trước rồi đặt câu hỏi.
- [ ] **Checkpoint:** Chạy được luồng `ingest → retrieve → answer`, câu trả lời có nguồn và trường hợp không đủ dữ liệu được xử lý rõ ràng.

---

## Definition of Done

- [ ] Có thể tìm top-k chunks liên quan từ collection Qdrant bằng câu hỏi tự nhiên.
- [ ] Kết quả truy hồi giữ metadata cần thiết để chỉ ra tên file và trang/đoạn.
- [ ] Unit test chạy mà không cần gọi dịch vụ bên ngoài.
- [ ] Câu trả lời RAG dựa trên context truy hồi và có tham chiếu nguồn.
- [ ] Khi không tìm thấy căn cứ, ứng dụng nói rõ thay vì tự tạo câu trả lời.
- [ ] `.env`, API key, `venv/`, `__pycache__/` không được đưa vào Git.

## Gợi ý mở rộng nếu hoàn thành sớm

- So sánh chất lượng với các giá trị `TOP_K` khác nhau.
- Thêm ngưỡng điểm tối thiểu để bỏ kết quả quá xa câu hỏi; kiểm tra cách score được định nghĩa trước khi đặt ngưỡng.
- Thử hybrid search (dense + sparse) hoặc reranking sau khi baseline retrieval đã có test đánh giá.
- Thêm streaming câu trả lời sau khi luồng hỏi đáp không streaming chạy ổn định.

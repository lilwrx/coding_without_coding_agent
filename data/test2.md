# Chính sách Bảo mật Thông tin Doanh nghiệp

*Phiên bản: 2.1*  
*Ngày hiệu lực: 01/01/2026*

## 1. Mục đích và Phạm vi
Chính sách này quy định các tiêu chuẩn bảo mật thông tin bắt buộc áp dụng đối với tất cả cán bộ nhân viên, đối tác và các hệ thống công nghệ thông tin của tổ chức.

## 2. Nguyên tắc phân loại dữ liệu
Dữ liệu trong hệ thống được chia thành 4 cấp độ bảo mật chính để phục vụ cho công tác kiểm soát truy cập và phân quyền ingest:

1. **Công khai (Public)**: Thông tin có thể chia sẻ rộng rãi ra bên ngoài tổ chức.
2. **Nội bộ (Internal)**: Tài liệu vận hành chung, chỉ sử dụng trong nội bộ công ty.
3. **Mật (Confidential)**: Dữ liệu tài chính, chiến lược kinh doanh, thông tin nhân sự.
4. **Tối mật (Restricted)**: Mã nguồn độc quyền, khóa bí mật, dữ liệu khách hàng cốt lõi.

---

## 3. Quy định về xử lý dữ liệu đưa vào hệ thống AI
Khi thực hiện nạp dữ liệu (ingest) vào các mô hình ngôn ngữ lớn (LLM) hoặc hệ thống RAG nội bộ, các đơn vị cần tuân thủ nghiêm ngặt:

- **Tuyệt đối không** đưa dữ liệu thuộc nhóm *Mật* và *Tối mật* vào các dịch vụ đám mây công cộng chưa được cấp phép.
- Mọi dữ liệu nhạy cảm phải được che giấu (masking) hoặc mã hóa trước khi xử lý qua các pipeline tự động.

> **Lưu ý quan trọng**: Vi phạm các quy định về bảo mật thông tin có thể dẫn đến hình thức kỷ luật lao động hoặc truy cứu trách nhiệm theo quy định pháp luật hiện hành.
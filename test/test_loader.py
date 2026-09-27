from loader import DocumentLoader
import pytest

@pytest.fixture
def sample_txt_file(tmp_path):
    """Fixture tạo file TXT tạm thời dùng cho các bài test"""
    file_path = tmp_path / "test_data.txt"
    file_path.write_text("Nội dung thử nghiệm bằng Pytest.", encoding="utf-8")
    return str(file_path)

def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        DocumentLoader.load_document("File_khong_ton_tai.pdf")

def test_unsupported_extension(tmp_path):
    """Kiểm tra ngoại lệ với định dạng không hỗ trợ (không truyền password)"""
    unsupported_file = tmp_path / "test.png"
    unsupported_file.write_bytes(b"fake image content")

    with pytest.raises(ValueError) as exc_info:
        DocumentLoader.load_document(str(unsupported_file))

    assert "chưa được hỗ trợ" in str(exc_info.value)
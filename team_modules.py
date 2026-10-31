"""Phần Triệu: nạp các module của bạn trong nhóm theo đúng tên/vị trí trên nhánh main.

Vì sao cần file này?
- Lõi A5/1 của Trâm Anh trên main tên là a51_core.py  -> import bình thường.
- Lõi TinyA5/1 của Bắp nằm ở core_bap/tiny_a5 và KHÔNG có đuôi .py,
  nên lệnh "import" thông thường không tìm thấy. Ở đây nạp file theo đường dẫn.
- Module file của Hằng (file_io_hang.py) hiện chạy thử mã hóa ngay khi bị import.
  Trước khi import, ta kiểm tra điều đó để không vô tình ghi đè file của Hằng.

File này KHÔNG sửa, KHÔNG sao chép code của các bạn; chỉ tìm và nạp đúng file.
"""
import ast
import importlib.machinery
import importlib.util
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
TINY_PATH = os.path.join(ROOT, "core_bap", "tiny_a5")
FILE_IO_PATH = os.path.join(ROOT, "file_io_hang.py")
TESTS_DIR = os.path.join(ROOT, "tests")

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import a51_core  # noqa: E402  (lõi A5/1 của Trâm Anh)


def load_tiny_module():
    """Nạp core_bap/tiny_a5 của Bắp, trả về module chứa class TinyA51."""
    if "tiny_a5" in sys.modules:
        return sys.modules["tiny_a5"]
    if not os.path.exists(TINY_PATH):
        raise FileNotFoundError("Không thấy core_bap/tiny_a5 (lõi TinyA5/1 của Bắp).")
    loader = importlib.machinery.SourceFileLoader("tiny_a5", TINY_PATH)
    spec = importlib.util.spec_from_loader("tiny_a5", loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    # Đăng viết test "from tiny_a5 import TinyA51"; đăng ký tên này để test
    # của Đăng chạy trên đúng lõi của Bắp thay vì một bản sao khác.
    sys.modules["tiny_a5"] = module
    return module


TinyA51 = load_tiny_module().TinyA51


def file_io_problem():
    """Trả về None nếu import file_io_hang an toàn, ngược lại trả về lý do."""
    if not os.path.exists(FILE_IO_PATH):
        return "Chưa có file_io_hang.py trong thư mục dự án."
    with open(FILE_IO_PATH, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    for node in tree.body:
        # Lệnh gọi hàm hoặc gán biến nằm trần ở cấp module sẽ chạy ngay khi import.
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            return (f"file_io_hang.py dòng {node.lineno} tự chạy mã hóa/giải mã khi import. "
                    "Cần Hằng chuyển các dòng chạy thử vào khối "
                    "'if __name__ == \"__main__\":'.")
    return None


def load_file_io():
    problem = file_io_problem()
    if problem:
        raise RuntimeError(problem)
    import file_io_hang
    return file_io_hang

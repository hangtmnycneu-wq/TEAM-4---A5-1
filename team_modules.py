"""Phần Triệu: tìm và nạp module của các bạn trong nhóm, ở bất kỳ vị trí nào nhóm đã đặt.

Vì sao cần file này?
- Vị trí hai lõi đã đổi nhiều lần trên GitHub:
    lõi A5/1 (Trâm Anh):   a51_core.py   ->  tests/a51_core.py   (Đăng chuyển ngày 05/11)
    lõi TinyA5/1 (Bắp):    core_bap/tiny_a5 (không đuôi .py)  ->  tests/tiny_a5.py
  Tệp này thử lần lượt từng vị trí trong danh sách, nạp tệp đầu tiên tìm thấy,
  và đăng ký với Python dưới tên "a51_core" / "tiny_a5". Nhờ vậy mọi tệp khác
  (của Triệu, Hằng, Trâm Anh, Đăng) viết "import a51_core" đều dùng đúng một lõi.
- Module file của Hằng (file_io_hang.py) hiện chạy thử mã hóa ngay khi bị import.
  Trước khi import, ta kiểm tra điều đó để không vô tình ghi đè file của Hằng.
- Công cụ đo hiệu năng của Trâm Anh (benchmark_a51.py) chỉ được gọi khi đã có trên nhánh.

Mọi tệp của Triệu phải "import team_modules" TRƯỚC khi "from a51_core import ...".
Tệp này KHÔNG sửa, KHÔNG sao chép code của các bạn; chỉ tìm và nạp đúng file.
"""
import ast
import importlib.machinery
import importlib.util
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
FILE_IO_PATH = os.path.join(ROOT, "file_io_hang.py")
TESTS_DIR = os.path.join(ROOT, "tests")
BENCHMARK_PATH = os.path.join(ROOT, "benchmark_a51.py")

# Các vị trí có thể có, thử theo thứ tự từ trên xuống.
A51_CANDIDATES = ["a51_core.py", os.path.join("tests", "a51_core.py")]
TINY_CANDIDATES = ["tiny_a5.py", os.path.join("core_bap", "tiny_a5"),
                   os.path.join("tests", "tiny_a5.py")]

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

LOADED_FROM = {}  # tên module -> đường dẫn tương đối đã nạp (để in ra khi demo)


def _load_core(name, candidates, owner):
    """Nạp tệp đầu tiên tồn tại trong candidates và đăng ký nó dưới tên name."""
    if name in sys.modules:
        return sys.modules[name]
    for rel in candidates:
        path = os.path.join(ROOT, rel)
        if os.path.isfile(path):
            loader = importlib.machinery.SourceFileLoader(name, path)
            spec = importlib.util.spec_from_loader(name, loader)
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module  # đăng ký trước để các tệp khác import cùng một lõi
            try:
                loader.exec_module(module)
            except Exception:
                del sys.modules[name]
                raise
            LOADED_FROM[name] = rel
            return module
    raise FileNotFoundError(f"Không tìm thấy lõi {name} của {owner}. Đã tìm ở: "
                            + ", ".join(candidates))


a51_core = _load_core("a51_core", A51_CANDIDATES, "Trâm Anh")
TinyA51 = _load_core("tiny_a5", TINY_CANDIDATES, "Bắp").TinyA51


def _call_on_import(path):
    """Trả về số dòng của lệnh gọi hàm nằm trần ở cấp module (sẽ tự chạy khi import)."""
    with open(path, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    for node in tree.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            return node.lineno
    return None


def file_io_problem():
    """Trả về None nếu import file_io_hang an toàn, ngược lại trả về lý do."""
    if not os.path.exists(FILE_IO_PATH):
        return "Chưa có file_io_hang.py trong thư mục dự án."
    line = _call_on_import(FILE_IO_PATH)
    if line:
        return (f"file_io_hang.py dòng {line} tự chạy mã hóa/giải mã khi import. "
                "Cần Hằng chuyển các dòng chạy thử vào khối "
                "'if __name__ == \"__main__\":'.")
    return None


def benchmark_problem():
    """Trả về None nếu gọi được benchmark_a51.py của Trâm Anh, ngược lại trả về lý do."""
    if not os.path.exists(BENCHMARK_PATH):
        return ("Chưa có benchmark_a51.py trên nhánh này "
                "(file của Trâm Anh đang ở nhánh a51-core, chưa merge vào main).")
    line = _call_on_import(BENCHMARK_PATH)
    if line:
        return f"benchmark_a51.py dòng {line} tự chạy khi import."
    return None


def load_benchmark():
    problem = benchmark_problem()
    if problem:
        raise RuntimeError(problem)
    import benchmark_a51
    return benchmark_a51


def load_file_io():
    problem = file_io_problem()
    if problem:
        raise RuntimeError(problem)
    import file_io_hang
    return file_io_hang

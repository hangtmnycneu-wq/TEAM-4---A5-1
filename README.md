# Nhóm 4 - Mô phỏng và phân tích hệ mã dòng A5/1

## 1. Thông tin đề tài

- **Tên đề tài:** Tìm hiểu, cài đặt và phân tích độ an toàn của hệ mã dòng **A5/1** (kèm phiên bản thu nhỏ **TinyA5/1** để minh họa và tấn công).
- **Môn học:** An toàn và Bảo mật thông tin (ATBMTT).
- **Ngôn ngữ:** Python 3 (chỉ dùng thư viện chuẩn, không phải cài thêm gói nào).
- **Mã nguồn:** toàn bộ được đẩy lên GitHub; đóng góp của từng thành viên thể hiện qua lịch sử commit.

## 2. Thành viên và phân công

Bảng dưới đây tổng hợp phân công của cả 5 thành viên. Chi tiết đóng góp theo thời gian xem thêm ở lịch sử commit trên GitHub.

| Thành viên | Phụ trách (code + báo cáo) | File chính phụ trách | Mức độ tham gia |
|---|---|---|---|
| **Minh Hằng** (nhóm trưởng) | Mô tả thuật toán A5/1 (lý thuyết); mã hóa/giải mã tệp; điều phối nhóm và tổng hợp báo cáo | `file_io_hang.py` |  |
| **Nguyễn Ngọc Trâm Anh** | Bối cảnh ra đời A5/1; lõi A5/1 đầy đủ; đo hiệu năng và kết quả thực nghiệm | `a51_core.py`, `benchmark_a51.py` |  |
| **Ngô Phương Anh** | Lõi TinyA5/1; ví dụ tính tay TinyA5/1 | `tiny_a5.py` |  |
| **Trịnh Hải Đăng** | So sánh A5/1 với các mã dòng khác; bộ kiểm thử (test vector, kiểm chứng hai lõi) | `tests/`, `test_demo.py` |  |
| **Nguyễn Quang Triệu** | Giao diện CLI và tích hợp module; kịch bản tấn công; phân tích độ an toàn | `main.py`, `attack_bruteforce.py`, `attack_demo.py` |  |

## 3. Cấu trúc thư mục dự án

```
TEAM-4---A5-1/
├─ main.py                 # Giao diện menu CLI, tích hợp các module
├─ a51_core.py             # Lõi A5/1 đầy đủ
├─ tiny_a5.py              # Lõi TinyA5/1 (23 bit)
├─ file_io_hang.py         # Mã hóa / giải mã tệp
├─ benchmark_a51.py        # Đo hiệu năng A5/1
├─ attack_bruteforce.py    # Tấn công vét cạn khóa TinyA5/1
├─ attack_demo.py          # Minh họa lỗi dùng lại dòng khóa
├─ test_demo.py            # Script kiểm thử tổng hợp (chạy riêng)
├─ tests/                  # Bộ kiểm thử bằng unittest
│  ├─ test_a51_core.py
│  ├─ test_cli_attack.py
│  └─ test_tiny_a51.py
├─ logo.png, logo_encrypted.bin, logo_decrypted.png, test.txt, test_encrypted.bin, test_decrypted.txt   # Tệp mẫu để demo (chức năng 3)
├─ test_results.txt        # Kết quả chạy bộ kiểm thử
└─ README.md
```

Vai trò và người phụ trách từng file:

| File | Vai trò | Người phụ trách |
|---|---|---|
| `main.py` | Giao diện menu dòng lệnh (CLI); chỉ nhận dữ liệu, kiểm tra và gọi các module lõi, không chứa logic mật mã | Triệu |
| `a51_core.py` | Lõi A5/1 đầy đủ: ba thanh ghi LFSR, nhịp đa số, mã hóa/giải mã | Trâm Anh |
| `tiny_a5.py` | Lõi TinyA5/1 (khóa 23 bit) dùng để minh họa từng bước và để tấn công vét cạn | Ngô Phương Anh (Bắp) |
| `file_io_hang.py` | Mã hóa / giải mã tệp (văn bản và ảnh) | Hằng |
| `benchmark_a51.py` | Đo thời gian mã hóa/giải mã A5/1 theo nhiều kích thước dữ liệu | Trâm Anh |
| `attack_bruteforce.py` | Tấn công vét cạn khóa TinyA5/1 khi biết một phần bản rõ | Triệu |
| `attack_demo.py` | Minh họa lỗi dùng lại dòng khóa (two-time pad) | Triệu |
| `tests/test_a51_core.py` | Kiểm thử lõi A5/1 bằng test vector chuẩn | Trịnh Hải Đăng (Đăng) |
| `tests/test_tiny_a51.py` | Kiểm thử lõi TinyA5/1 | Trịnh Hải Đăng (Đăng) |
| `tests/test_cli_attack.py` | Kiểm thử giao diện CLI và phần tấn công | Triệu |
| `test_demo.py` | Script kiểm thử tổng hợp, chạy riêng (không thuộc `tests/`) | Trịnh Hải Đăng (Đăng) |
| `logo.png`, `logo_encrypted.bin`, `logo_decrypted.png`, `test.txt` | Tệp mẫu để demo mã hóa/giải mã (chức năng 3) | dữ liệu dùng chung |
| `test_results.txt` | Kết quả chạy bộ kiểm thử | Đăng |

## 4. Yêu cầu môi trường

- **Python 3** (khuyến nghị 3.10 trở lên).
- Không cần cài thêm thư viện: chương trình chỉ dùng thư viện chuẩn của Python.

## 5. Hướng dẫn cài đặt và chạy chương trình

Tải mã nguồn và vào thư mục dự án:

```bash
git clone https://github.com/hangtmnycneu-wq/TEAM-4---A5-1.git
cd TEAM-4---A5-1
```

Chạy chương trình chính (menu điều khiển toàn bộ demo):

```bash
python3 main.py
```

Chương trình hiện một menu; nhập số tương ứng để chọn chức năng. Tại các ô nhập có ghi `[Enter dùng ...]`, chỉ cần nhấn Enter để dùng giá trị mặc định.

Chạy bộ kiểm thử (tùy chọn):

```bash
python3 -m unittest discover -s tests   # chạy 3 file trong tests/ (24 test)
python3 test_demo.py                     # chạy script kiểm thử tổng hợp riêng
```

## 6. Các chức năng trên menu

| Số | Chức năng | Gọi module của |
|---|---|---|
| 1 | TinyA5/1: in trạng thái từng bước | Bắp |
| 2 | A5/1: mã hóa / giải mã chuỗi văn bản | Trâm Anh |
| 3 | Mã hóa / giải mã tệp (văn bản, ảnh) | Hằng |
| 4 | Chạy bộ kiểm thử trong `tests/` | Đăng |
| 5 | Tấn công vét cạn khóa TinyA5/1 | Triệu |
| 6 | Minh họa lỗi dùng lại dòng khóa (two-time pad) | Triệu |
| 7 | Đo hiệu năng mã hóa/giải mã A5/1 | Trâm Anh |
| 0 | Thoát chương trình | |

Phần giao diện được tách hoàn toàn khỏi phần thuật toán: `main.py` chỉ điều phối, còn mọi logic mật mã nằm trong các module lõi do từng thành viên xây dựng.

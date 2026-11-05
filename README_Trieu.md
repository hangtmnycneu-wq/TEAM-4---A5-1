# Phần của Triệu: giao diện CLI, tích hợp và minh họa tấn công

Phụ trách: Nguyễn Quang Triệu — phân tích độ an toàn, giao diện CLI, tích hợp module, minh họa tấn công.
Có dùng AI (ChatGPT, Claude) hỗ trợ viết menu, mô phỏng tấn công và kiểm tra tích hợp; Triệu đọc, chạy và giải thích được toàn bộ mã dưới đây. Lõi mật mã là của Trâm Anh và Bắp, không bị sửa.

## Các file của Triệu

| File | Vai trò |
|---|---|
| `main.py` | Menu CLI; chỉ hỏi dữ liệu, kiểm tra và gọi module của các bạn |
| `team_modules.py` | Tìm và nạp đúng module trên main: `a51_core.py` (Trâm Anh), `core_bap/tiny_a5` (Bắp, file không có đuôi .py), `file_io_hang.py` (Hằng) |
| `attack_bruteforce.py` | **Tấn công vét cạn khóa TinyA5/1 khi biết một phần bản rõ** — kiểu tấn công thuộc phần I |
| `attack_demo.py` | Minh họa lỗi dùng lại dòng khóa (phần bổ sung, chờ nhóm quyết giữ hay bỏ) |
| `check_integration.py` | 10 nhóm kiểm tra tích hợp; không thay bộ test của Đăng |

## Cách chạy

Đặt các file trên vào **thư mục gốc repository** (cùng chỗ với `a51_core.py` và thư mục `core_bap/`). Cần Python 3, không cài thêm thư viện.

```bash
python3 main.py              # menu
python3 check_integration.py # kiểm tra tích hợp
python3 attack_bruteforce.py # chạy riêng demo vét cạn (khoảng 10–30 giây tùy máy)
```

## Menu

| Số | Chức năng | Gọi module của |
|---|---|---|
| 1 | TinyA5/1 in từng bước (mặc định K=10010101001110100110000, P=111 → S=100, C=011) | Bắp |
| 2 | A5/1 mã hóa / giải mã chuỗi văn bản | Trâm Anh |
| 3 | Mã hóa / giải mã file (văn bản, ảnh) | Hằng |
| 4 | Chạy bộ kiểm thử trong `tests/` | Đăng |
| 5 | Tấn công vét cạn khóa TinyA5/1 | Triệu (dùng lõi Bắp) |
| 6 | Minh họa dùng lại dòng khóa | Triệu (dùng lõi Trâm Anh) |

Menu 3 và 4 không giả chức năng: nếu module chưa sẵn sàng, chương trình nói rõ lý do.

- Menu 3 hiện báo: `file_io_hang.py` tự chạy mã hóa/giải mã ngay khi bị import (các dòng cuối file nằm ngoài khối `if __name__ == "__main__":`). Khi Hằng chuyển các dòng đó vào khối này, menu 3 tự hoạt động. Đã thử trên bản sao: mã hóa rồi giải mã `logo.png` cho ảnh giống hệt bản gốc.
- Menu 4 chạy được khi thư mục `tests/` của Đăng có trên main. Đã thử với `tests/` lấy từ nhánh `Dang-test-suite`: 14 test qua, gồm test vector A5/1.

## Demo tấn công vét cạn (menu 5)

1. Người gửi mã hóa `"GSM:HEN 9H"` (80 bit) bằng lõi Tiny của Bắp với khóa bí mật 23 bit.
2. Kẻ tấn công có bản mã và biết phần đầu `"GSM:"` (32 bit).
3. Tính `S = P XOR C` cho 32 bit đầu → biết 32 bit dòng khóa.
4. Thử cả 2^23 = 8.388.608 khóa; khóa nào sinh đúng 32 bit đó là ứng viên. Đa số khóa sai bị loại sau 1–2 bit.
5. Dùng khóa tìm được giải mã toàn bộ bản tin, lộ phần bí mật `"HEN 9H"`.

Kết quả chạy thật (môi trường thử, Python 3.13): 13,3 giây, 1 ứng viên duy nhất và đúng khóa thật. Nếu chỉ dùng 16 bit đã biết thì có 150 khóa cùng khớp — minh họa vì sao cần đủ bản rõ đã biết (khoảng ≥ độ dài khóa). Tốc độ máy khác sẽ khác.

Hàm `brute_force_tiny` chỉ nhận bản rõ đã biết, bản mã và (tuỳ chọn) phần khóa giả định đã biết để thu nhỏ không gian khi demo bị giới hạn thời gian. Không nhận khóa bí mật. Kẻ tấn công tự cài lại bộ sinh Tiny bằng số nguyên (vì thuật toán công khai); bộ này được kiểm tra khớp từng bit với lõi của Bắp trên 500 khóa ngẫu nhiên × 64 bit.

## Giới hạn cần nói rõ

- Vét cạn chỉ khả thi vì Tiny có 23 bit khóa. Con số ngoại suy cho A5/1 (2^54, 2^64) chỉ để so sánh độ lớn, không phải đo thực.
- Kết quả Tiny phụ thuộc quy tắc trong code của Bắp (majority x1, y3, z3…). Phần mô tả của Hằng trong DOCX ghi quy tắc khác; nhóm cần chốt theo slide bài giảng.
- Lõi A5/1 khớp test vector tham chiếu (khóa 1223456789ABCDEF, frame 0x134) khi khóa hex được chuyển theo thứ tự bit thấp trước trong từng byte (test của Đăng). Menu 2 nhận trực tiếp chuỗi 64 bit, không đổi hex.
- Lõi không chia dữ liệu dài thành các khung 228 bit như GSM thật và không có xác thực toàn vẹn.

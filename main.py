"""Menu CLI Nhóm 4 - A5/1 (phần Triệu). Chạy: python3 main.py

main.py chỉ hỏi dữ liệu, kiểm tra và GỌI module của các bạn, không chứa thuật toán:
- a51_core.py           : lõi A5/1 đầy đủ (Trâm Anh)
- tiny_a5.py            : lõi TinyA5/1 (Bắp)
- file_io_hang.py       : mã hóa/giải mã tệp (Hằng)
- benchmark_a51.py      : đo hiệu năng A5/1 (Trâm Anh)
- tests/                : bộ kiểm thử (Đăng + phần kiểm thử của Triệu)
- attack_bruteforce.py  : tấn công vét cạn khóa TinyA5/1 (Triệu)
- attack_demo.py        : minh họa lỗi dùng lại dòng khóa (Triệu)

Hai lõi và benchmark được nhập ở đầu file (đều ở thư mục gốc dự án). Riêng
file_io_hang.py được nhập ngay trong mục 3 để nếu tệp này chưa sẵn sàng thì
chỉ mục 3 bị ảnh hưởng, cả chương trình vẫn chạy.
"""
import os
import unittest

import benchmark_a51
from a51_core import crypt_bits, encrypt_text
from attack_bruteforce import KEY_BITS, run_bruteforce_demo
from attack_demo import DEMO_KEY, decode_bits_strict, run_attack_demo, validate_bits
from tiny_a5 import TinyA51

ROOT = os.path.dirname(os.path.abspath(__file__))
TESTS_DIR = os.path.join(ROOT, "tests")


def ask(label: str, default: str) -> str:
    value = input(f"{label} [Enter dùng {default}]: ").strip()
    return value if value != "" else default


def run_tiny() -> None:
    key = ask("Khóa 23 bit", "10010101001110100110000")
    plain = ask("Bản rõ dạng bit", "111")
    validate_bits(plain)
    # Dùng hai đối tượng để giải mã bắt đầu lại từ đúng trạng thái ban đầu.
    cipher, stream = TinyA51(key).encrypt_decrypt(plain, verbose=True)
    restored, _ = TinyA51(key).encrypt_decrypt(cipher)
    print("Dòng khóa:", stream)
    print("Bản mã   :", cipher)
    print("Giải mã  :", restored)
    print("Khớp gốc :", restored == plain)


def run_standard() -> None:
    action = ask("1 = mã hóa; 2 = giải mã", "1")
    if action not in {"1", "2"}:
        raise ValueError("Chọn 1 hoặc 2.")
    key = ask("Khóa 64 bit", DEMO_KEY)
    frame = int(ask("Số khung (frame, 0 đến 2^22-1)", "1"))
    if action == "1":
        text = ask("Bản rõ", "Xin chao Nhom 4!")
        cipher = encrypt_text(text, key, frame)
        restored = decode_bits_strict(crypt_bits(cipher, key, frame))
        print("Bản mã dạng bit:", cipher)
        print("Giải mã lại    :", restored)
        print("Khớp gốc       :", restored == text)
    else:
        cipher = input("Dán bản mã dạng bit: ").strip()
        validate_bits(cipher)
        if len(cipher) % 8:
            raise ValueError("Bản mã văn bản phải có số bit chia hết cho 8.")
        print("Bản rõ:", decode_bits_strict(crypt_bits(cipher, key, frame)))


def run_file() -> None:
    # Nhập module của Hằng tại đây (không ở đầu file): nếu tệp chưa được sửa để
    # không tự chạy khi nhập, hoặc thiếu tệp mẫu, thì chỉ mục này báo lỗi.
    try:
        import file_io_hang
    except (ImportError, FileNotFoundError, ValueError, UnicodeDecodeError) as error:
        print("Chưa gọi được module file của Hằng:", error)
        return
    src = ask("Tệp đầu vào", os.path.join(ROOT, "test.txt"))
    dst = ask("Tệp đầu ra", src + ".a51")
    if os.path.abspath(src) == os.path.abspath(dst):
        raise ValueError("Tệp đầu ra phải khác tệp đầu vào.")
    key = ask("Khóa 64 bit", DEMO_KEY)
    frame = int(ask("Số khung (frame)", "1"))
    file_io_hang.process_file_a51(src, dst, key, frame)
    print("Chạy lại chức năng này với tệp đầu ra (cùng khóa, frame) để giải mã.")


def run_team_tests() -> None:
    suite = unittest.defaultTestLoader.discover(TESTS_DIR, pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    print("Bộ kiểm thử của nhóm:", "QUA" if result.wasSuccessful() else "CÓ LỖI")


def run_benchmark() -> None:
    print("Đo thời gian mã hóa/giải mã A5/1 từ 100 byte đến 500 KB (khoảng 20-30 giây)...")
    benchmark_a51.benchmark_performance()


def run_bruteforce() -> None:
    bits = int(ask("Số bit khóa chưa biết (1-23; 23 = vét cạn toàn bộ)", str(KEY_BITS)))
    run_bruteforce_demo(bits)


def main() -> None:
    while True:
        print("\n=== NHÓM 4 - MENU A5/1 ===")
        print("1. TinyA5/1 - xem từng bước")
        print("2. A5/1 - mã hóa và giải mã chuỗi")
        print("3. A5/1 - mã hóa/giải mã tệp (module Hằng)")
        print("4. Chạy bộ kiểm thử của nhóm (thư mục tests/)")
        print("5. Tấn công vét cạn khóa TinyA5/1")
        print("6. Minh họa lỗi dùng lại dòng khóa")
        print("7. Đo hiệu năng A5/1 (module Trâm Anh)")
        print("0. Thoát")
        try:
            choice = input("Chọn: ").strip()
            if choice == "0":
                print("Đã thoát.")
                return
            actions = {"1": run_tiny, "2": run_standard, "3": run_file,
                       "4": run_team_tests, "5": run_bruteforce, "6": run_attack_demo,
                       "7": run_benchmark}
            if choice in actions:
                actions[choice]()
            else:
                print("Lựa chọn không hợp lệ. Nhập từ 0 đến 7.")
        except UnicodeDecodeError:
            print("Không đọc được UTF-8. Kiểm tra khóa, frame và bản mã; dữ liệu có thể sai.")
        except (ValueError, FileNotFoundError) as error:
            print("Dữ liệu không hợp lệ:", error)
        except (EOFError, KeyboardInterrupt):
            print("\nĐã thoát.")
            return


if __name__ == "__main__":
    main()

"""Menu CLI Nhóm 4 - A5/1 (phần Triệu). Chạy: python3 main.py

main.py chỉ hỏi dữ liệu, kiểm tra và GỌI module của các bạn:
- a51_core              : lõi A5/1 đầy đủ (Trâm Anh)      } team_modules.py tự tìm ở thư mục gốc,
- tiny_a5               : lõi TinyA5/1 (Bắp)              } core_bap/ hoặc tests/
- file_io_hang.py       : mã hóa/giải mã file (Hằng)
- tests/                : bộ kiểm thử (Đăng), nếu đã có trên nhánh đang chạy
- attack_bruteforce.py  : tấn công vét cạn khóa TinyA5/1 (Triệu)
- attack_demo.py        : minh họa lỗi dùng lại dòng khóa (Triệu)
- benchmark_a51.py      : đo hiệu năng A5/1 (Trâm Anh), nếu đã có trên nhánh đang chạy
"""
import os
import unittest

import team_modules  # noqa: F401  (tìm và nạp lõi của nhóm TRƯỚC mọi import khác)
from a51_core import crypt_bits, encrypt_text
from attack_bruteforce import KEY_BITS, run_bruteforce_demo
from attack_demo import DEMO_KEY, decode_bits_strict, run_attack_demo, validate_bits
from team_modules import (ROOT, TESTS_DIR, TinyA51, benchmark_problem, file_io_problem,
                          load_benchmark, load_file_io)


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
    problem = file_io_problem()
    if problem:
        print("Chưa gọi được module file của Hằng:", problem)
        return
    file_io = load_file_io()
    src = ask("File đầu vào", os.path.join(ROOT, "test.txt"))
    dst = ask("File đầu ra", src + ".a51")
    if os.path.abspath(src) == os.path.abspath(dst):
        raise ValueError("File đầu ra phải khác file đầu vào.")
    key = ask("Khóa 64 bit", DEMO_KEY)
    frame = int(ask("Số khung (frame)", "1"))
    file_io.process_file_a51(src, dst, key, frame)
    print("Chạy lại chức năng này với file đầu ra (cùng khóa, frame) để giải mã.")


def run_team_tests() -> None:
    if not os.path.isdir(TESTS_DIR):
        print("Chưa có thư mục tests/ của Đăng trên nhánh này (chưa merge vào main).")
        return
    # Test của Đăng import a51_core và tiny_a5; team_modules đã đưa thư mục gốc vào
    # đường dẫn tìm module và đăng ký tiny_a5 = lõi core_bap/tiny_a5 của Bắp.
    suite = unittest.defaultTestLoader.discover(TESTS_DIR, pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    print("Bộ test của Đăng:", "QUA" if result.wasSuccessful() else "CÓ LỖI")


def run_benchmark() -> None:
    problem = benchmark_problem()
    if problem:
        print("Chưa gọi được công cụ đo hiệu năng của Trâm Anh:", problem)
        return
    print("Đo thời gian mã hóa/giải mã A5/1 từ 100 byte đến 500 KB (khoảng 20-30 giây)...")
    load_benchmark().benchmark_performance()


def run_bruteforce() -> None:
    bits = int(ask("Số bit khóa chưa biết (1-23; 23 = vét cạn toàn bộ)", str(KEY_BITS)))
    run_bruteforce_demo(bits)


def main() -> None:
    print("Lõi A5/1:", team_modules.LOADED_FROM["a51_core"],
          "| Lõi TinyA5/1:", team_modules.LOADED_FROM["tiny_a5"])
    while True:
        print("\n=== NHÓM 4 - MENU A5/1 ===")
        print("1. TinyA5/1 - xem từng bước")
        print("2. A5/1 - mã hóa và giải mã chuỗi")
        print("3. A5/1 - mã hóa/giải mã file (module Hằng)")
        print("4. Chạy bộ kiểm thử (module Đăng)")
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

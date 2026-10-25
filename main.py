"""Menu CLI của Triệu. Chạy bằng python3 main.py."""
from tinya51 import TinyA51
from a51_standard import encrypt_text, crypt_bits
from attack_demo import (DEMO_KEY, validate_bits, decode_bits_strict,
                         run_attack_demo)


def ask(label: str, default: str) -> str:
    value = input(f"{label} [Enter dùng {default}]: ")
    return value if value != "" else default


def run_tiny() -> None:
    key = ask("Khóa 23 bit", "10010101001110100110000")
    plain = ask("Bản rõ dạng bit", "111")
    validate_bits(plain)
    # Dùng hai đối tượng để giải mã bắt đầu từ đúng trạng thái ban đầu.
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
    frame = int(ask("Giá trị frame nạp vào lõi", "1"))
    print("Dùng bộ sinh Trâm Anh cung cấp; chưa đối chiếu vector chuẩn ngoài.")
    if action == "1":
        text = ask("Bản rõ", "Xin chao Trieu!")
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


def main() -> None:
    while True:
        print("\n=== NHÓM 4 — MENU A5/1 CỦA TRIỆU ===")
        print("1. TinyA5/1 — xem từng bước")
        print("2. A5/1 — mã hóa và giải mã chuỗi")
        print("3. Xử lý file — chờ module Hằng")
        print("4. Test suite của nhóm — chờ module Đăng")
        print("5. Demo dùng lại dòng khóa")
        print("0. Thoát")
        try:
            choice = input("Chọn: ").strip()
            if choice == "0":
                print("Đã thoát.")
                return
            if choice == "1":
                run_tiny()
            elif choice == "2":
                run_standard()
            elif choice in {"3", "4"}:
                print("Chưa tích hợp module tương ứng của thành viên phụ trách.")
            elif choice == "5":
                run_attack_demo()
            else:
                print("Lựa chọn không hợp lệ. Nhập 0, 1, 2, 3, 4 hoặc 5.")
        except UnicodeDecodeError:
            print("Không đọc được UTF-8. Kiểm tra khóa, frame và bản mã; dữ liệu có thể sai.")
        except ValueError as error:
            print("Dữ liệu không hợp lệ:", error)
        except (EOFError, KeyboardInterrupt):
            print("\nĐã thoát.")
            return


if __name__ == "__main__":
    main()

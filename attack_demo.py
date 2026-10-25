"""Phần Triệu: mô phỏng lỗi dùng lại dòng khóa trên module Trâm Anh.

Hàm tấn công không nhận khóa, dòng khóa hay bản rõ mục tiêu.
Demo 6 byte nằm trong 48 bit đầu, không mô phỏng dữ liệu nhiều khung.
"""
from a51_standard import crypt_bits, text_to_bits

DEMO_KEY = "1101010100111010011000110101010011101001100011010101001110100110"


def validate_bits(bits: str) -> None:
    if not isinstance(bits, str) or not set(bits) <= {"0", "1"}:
        raise ValueError("Dữ liệu phải là chuỗi chỉ chứa 0 và 1.")


def xor_bits(a: str, b: str) -> str:
    validate_bits(a)
    validate_bits(b)
    if len(a) != len(b):
        raise ValueError("Hai chuỗi XOR phải cùng độ dài.")
    return "".join(str(int(x) ^ int(y)) for x, y in zip(a, b))


def recover_reused_segment(c1: str, c2: str, known_p1: str,
                           offset: int = 0) -> str:
    """offset là vị trí bit; hai bản mã đã căn cùng vị trí dòng khóa."""
    for value in (c1, c2, known_p1):
        validate_bits(value)
    if type(offset) is not int or offset < 0:
        raise ValueError("Vị trí bắt đầu phải là số nguyên không âm.")
    end = offset + len(known_p1)
    if end > min(len(c1), len(c2)):
        raise ValueError("Đoạn đã biết vượt quá phạm vi hai bản mã.")
    return xor_bits(xor_bits(c1[offset:end], c2[offset:end]), known_p1)


def decode_bits_strict(bits: str) -> str:
    validate_bits(bits)
    if len(bits) % 8:
        raise ValueError("Dữ liệu văn bản phải có số bit chia hết cho 8.")
    return bytes(int(bits[i:i + 8], 2)
                 for i in range(0, len(bits), 8)).decode("utf-8")


def run_attack_demo() -> None:
    # Dữ liệu người gửi: ngắn để không phải thiết kế cách chuyển khung.
    p1_text, p2_text = "DON100", "DON900"
    p1, p2 = text_to_bits(p1_text), text_to_bits(p2_text)
    c1 = crypt_bits(p1, DEMO_KEY, frame=1)
    c2 = crypt_bits(p2, DEMO_KEY, frame=1)

    print("\nDEMO CỐ Ý DÙNG LẠI DÒNG KHÓA")
    print("Người gửi mã hóa hai bản tin bằng cùng khóa, frame và vị trí bắt đầu.")
    print("Kẻ tấn công chỉ nhận C1, C2 và P1 đã biết.")
    print("P1 đã biết:", p1_text)
    print("P1 bits   :", p1)
    print("C1        :", c1)
    print("C2        :", c2)
    print("C1 XOR C2 :", xor_bits(c1, c2))
    recovered = recover_reused_segment(c1, c2, p1)
    print("P2 suy ra :", recovered)
    print("P2 văn bản:", decode_bits_strict(recovered))
    print("Đối chiếu với P2 gốc SAU khi khôi phục:", recovered == p2)

    # Trường hợp đối chiếu: giữ khóa, đổi frame của bản tin thứ hai.
    different_c2 = crypt_bits(p2, DEMO_KEY, frame=2)
    guess = recover_reused_segment(c1, different_c2, p1)
    print("\nĐỐI CHIẾU: bản tin thứ hai dùng frame=2")
    print("Cách suy ra cũ còn khôi phục đúng P2 trong ví dụ này?", guess == p2)
    print("Kết luận: demo khai thác việc lặp dòng khóa; không tìm khóa bí mật.")


if __name__ == "__main__":
    run_attack_demo()

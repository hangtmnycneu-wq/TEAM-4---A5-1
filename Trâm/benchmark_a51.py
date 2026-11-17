import random
import string
import time

try:
    from a51_core import encrypt_text, decrypt_text
except ModuleNotFoundError as e:
    if e.name != "a51_core":
        raise
    raise SystemExit(
        "Không tìm thấy file 'a51_core.py'! "
        "Hãy đặt 'a51_core.py' và 'benchmark_a51.py' trong cùng một thư mục."
    )


# =========================================================
# TIỆN ÍCH
# =========================================================
def parse_key(raw: str) -> str:
    """Nhận khóa dạng 64 bit nhị phân hoặc 16 ký tự hex, trả về chuỗi 64 bit."""
    s = raw.strip().replace(" ", "").lower()
    if s.startswith("0x"):
        s = s[2:]
    if len(s) == 64 and set(s) <= {"0", "1"}:
        return s
    if len(s) == 16:
        try:
            return f"{int(s, 16):064b}"
        except ValueError:
            pass
    raise ValueError("Khóa phải là 64 bit nhị phân hoặc 16 ký tự hex.")


def bits_to_hex(bits: str) -> str:
    return f"{int(bits, 2):0{len(bits) // 4}x}"


def input_key() -> str:
    while True:
        try:
            return parse_key(input("Nhập khóa K (64 bit nhị phân hoặc 16 hex): "))
        except ValueError as err:
            print(f"  Lỗi: {err}")


def input_plaintext() -> str:
    while True:
        text = input("Nhập bản rõ P: ")
        if text:
            return text
        print("  Lỗi: bản rõ không được để trống.")


# =========================================================
# 1. DEMO MÃ HÓA VÀ GIẢI MÃ (NHẬP TỪ BÀN PHÍM)
# =========================================================
def run_demo():
    print("=" * 70)
    print("        DEMO MÃ HÓA VÀ GIẢI MÃ A5/1 CHUẨN")
    print("=" * 70)

    plaintext = input_plaintext()
    key = input_key()
    n_bytes = len(plaintext.encode("utf-8"))

    print(f"\nKhóa K (64-bit) : {key}")
    print(f"Bản rõ (P)      : {plaintext} ({n_bytes} bytes)")

    t0 = time.perf_counter()
    cipher_bits = encrypt_text(plaintext, key)
    t_enc = (time.perf_counter() - t0) * 1000

    print(f"Bản mã (bit)    : {cipher_bits[:64]}{'...' if len(cipher_bits) > 64 else ''} "
          f"({len(cipher_bits)} bits)")
    print(f"Bản mã (hex)    : {bits_to_hex(cipher_bits)}")
    print(f"Thời gian mã hóa: {t_enc:.4f} ms")

    t0 = time.perf_counter()
    decrypted = decrypt_text(cipher_bits, key)
    t_dec = (time.perf_counter() - t0) * 1000

    print(f"Văn bản giải mã : {decrypted}")
    print(f"Thời gian giải mã: {t_dec:.4f} ms")
    print(f"Kết quả kiểm tra: {'[THÀNH CÔNG]' if decrypted == plaintext else '[THẤT BẠI]'}")
    print("=" * 70 + "\n")


# =========================================================
# 2. PHÂN TÍCH HIỆU NĂNG
# =========================================================
def generate_random_text(size_in_bytes: int) -> str:
    """Sinh chuỗi ASCII ngẫu nhiên (1 ký tự = 1 byte UTF-8)."""
    chars = string.ascii_letters + string.digits + " \n\t"
    return "".join(random.choices(chars, k=size_in_bytes))


def benchmark_performance():
    random.seed(2024)  # kết quả dữ liệu mẫu lặp lại được
    key = "1101010100111010011000110101010011101001100011010101001110100110"

    test_sizes = [
        ("100 Bytes", 100),
        ("1 KB", 1024),
        ("10 KB", 10 * 1024),
        ("50 KB", 50 * 1024),
        ("100 KB", 100 * 1024),
        ("250 KB", 250 * 1024),
        ("500 KB", 500 * 1024),
    ]

    header = (f"{'Dung lượng':<10} | {'Bytes':>9} | {'Mã hóa (s)':>11} | "
              f"{'Giải mã (s)':>11} | {'Tốc độ (KB/s)':>13} | {'Đúng':^5}")
    line = "-" * len(header)

    print("=" * len(header))
    print("   PHÂN TÍCH HIỆU NĂNG A5/1 THEO DUNG LƯỢNG DỮ LIỆU")
    print("=" * len(header))
    print(header)
    print(line)

    for label, size in test_sizes:
        data = generate_random_text(size)          # sinh dữ liệu ngoài vùng đo
        repeats = 5 if size <= 10 * 1024 else 1    # mốc lớn rất chậm, chỉ đo 1 lần
        enc_times, dec_times, ok = [], [], True

        for _ in range(repeats):
            t0 = time.perf_counter()
            cipher = encrypt_text(data, key)
            enc_times.append(time.perf_counter() - t0)

            t0 = time.perf_counter()
            plain = decrypt_text(cipher, key)
            dec_times.append(time.perf_counter() - t0)

            ok = ok and (plain == data)

        t_enc, t_dec = min(enc_times), min(dec_times)
        speed_kb_s = (size / 1024) / t_enc if t_enc > 0 else 0.0

        print(f"{label:<10} | {size:>9,d} | {t_enc:>11.6f} | {t_dec:>11.6f} | "
              f"{speed_kb_s:>13.2f} | {'OK' if ok else 'SAI':^5}", flush=True)

    print(line)
    print("Ghi chú: đo bằng time.perf_counter(); mốc <= 10 KB lấy giá trị nhỏ nhất của 5 lần đo,")
    print("các mốc lớn đo 1 lần. Thời gian mã hóa gồm cả khởi tạo (186 nhịp) và đổi text <-> bit.\n")


# =========================================================
# CHƯƠNG TRÌNH CHÍNH
# =========================================================
if __name__ == "__main__":
    run_demo()
    if input("Chạy phân tích hiệu năng? Mốc lớn có thể mất vài phút (y/N): ").strip().lower() == "y":
        benchmark_performance()

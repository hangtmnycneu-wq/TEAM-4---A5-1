"""Phần Triệu: minh họa TẤN CÔNG VÉT CẠN KHÓA (biết bản rõ) trên TinyA5/1.

Kịch bản
--------
1. Người gửi mã hóa bản tin bằng lõi TinyA5/1 của Bắp với khóa bí mật 23 bit.
2. Kẻ tấn công thu được bản mã C và biết trước phần đầu bản tin P_head
   (ví dụ phần mở đầu cố định của mọi bản tin).
3. Kẻ tấn công tính S_head = P_head XOR C_head (đoạn dòng khóa tương ứng).
4. Thử lần lượt mọi khóa có thể; khóa nào sinh ra đúng S_head là ứng viên.
5. Dùng khóa tìm được giải mã PHẦN CÒN LẠI của bản tin mà kẻ tấn công chưa biết.

Hàm tấn công (brute_force_tiny) chỉ nhận bản rõ đã biết, bản mã và (tuỳ chọn)
phần khóa giả định đã biết để thu nhỏ không gian khi demo. Không nhận khóa bí mật.

Kẻ tấn công được biết thuật toán (nguyên lý Kerckhoffs), nên tự cài lại bộ sinh
Tiny bằng số nguyên cho nhanh (_tiny_bits). Bộ này được kiểm tra khớp từng bit với
lõi của Bắp trong check_integration.py; khóa tìm được cũng được xác nhận lại bằng
chính lõi của Bắp.
"""
import time

from attack_demo import validate_bits, xor_bits
from team_modules import TinyA51

KEY_BITS = 23


def _rev(value: int, width: int) -> int:
    """Đảo thứ tự bit. Khóa ghi x0 trước, còn số nguyên có x0 ở bit thấp nhất."""
    return int(f"{value:0{width}b}"[::-1], 2)


# Bảng tra sẵn để đổi nhanh khóa (số nguyên 23 bit) -> ba thanh ghi X, Y, Z.
_REV6 = [_rev(v, 6) for v in range(1 << 6)]
_REV8 = [_rev(v, 8) for v in range(1 << 8)]
_REV9 = [_rev(v, 9) for v in range(1 << 9)]


def _key_int_to_regs(k: int):
    """key = X(6 bit) | Y(8 bit) | Z(9 bit), giống cách Bắp chia key[0:6], [6:14], [14:23]."""
    return _REV6[k >> 17], _REV8[(k >> 9) & 0xFF], _REV9[k & 0x1FF]


def _tiny_bits(x: int, y: int, z: int, target: list) -> int:
    """Sinh dòng khóa Tiny và so với target; trả về số bit đầu tiên khớp liên tiếp.

    Quy tắc giống lõi của Bắp: majority(x1, y3, z3); phản hồi X = x2^x4^x5,
    Y = y6^y7, Z = z2^z7^z8; dịch để bit mới vào vị trí 0; đầu ra x5^y7^z8.
    Dừng ngay ở bit đầu tiên sai (đa số khóa sai bị loại sau 1-2 bit).
    """
    for i, want in enumerate(target):
        a, b, c = (x >> 1) & 1, (y >> 3) & 1, (z >> 3) & 1
        m = 1 if a + b + c >= 2 else 0
        if a == m:
            x = ((x << 1) | (((x >> 2) ^ (x >> 4) ^ (x >> 5)) & 1)) & 0x3F
        if b == m:
            y = ((y << 1) | (((y >> 6) ^ (y >> 7)) & 1)) & 0xFF
        if c == m:
            z = ((z << 1) | (((z >> 2) ^ (z >> 7) ^ (z >> 8)) & 1)) & 0x1FF
        if (((x >> 5) ^ (y >> 7) ^ (z >> 8)) & 1) != want:
            return i
    return len(target)


def fast_keystream(key: str, length: int) -> str:
    """Bản dùng cho kiểm thử: sinh dòng khóa bằng bộ sinh nhanh để so với lõi Bắp."""
    validate_bits(key)
    if len(key) != KEY_BITS:
        raise ValueError("Khóa Tiny phải đủ 23 bit.")
    x, y, z = _key_int_to_regs(int(key, 2))
    out = []
    for _ in range(length):  # cùng các bước như _tiny_bits, nhưng ghi lại mọi bit
        a, b, c = (x >> 1) & 1, (y >> 3) & 1, (z >> 3) & 1
        m = 1 if a + b + c >= 2 else 0
        if a == m:
            x = ((x << 1) | (((x >> 2) ^ (x >> 4) ^ (x >> 5)) & 1)) & 0x3F
        if b == m:
            y = ((y << 1) | (((y >> 6) ^ (y >> 7)) & 1)) & 0xFF
        if c == m:
            z = ((z << 1) | (((z >> 2) ^ (z >> 7) ^ (z >> 8)) & 1)) & 0x1FF
        out.append(str(((x >> 5) ^ (y >> 7) ^ (z >> 8)) & 1))
    return "".join(out)


def brute_force_tiny(known_plain: str, cipher: str, known_key_prefix: str = "",
                     weak_check_bits: int = 16, progress=None) -> dict:
    """Vét cạn khóa TinyA5/1 khi biết bản rõ ở đầu bản tin.

    known_plain      : các bit bản rõ đã biết, ứng với đầu bản mã.
    cipher           : bản mã (ít nhất dài bằng known_plain).
    known_key_prefix : (tuỳ chọn) các bit đầu khóa coi như đã biết, CHỈ để
                       thu nhỏ không gian khi demo có giới hạn thời gian.
    weak_check_bits  : đếm thêm số khóa khớp nếu chỉ dùng chừng này bit,
                       để minh họa vì sao cần đủ bản rõ đã biết.
    """
    validate_bits(known_plain)
    validate_bits(cipher)
    if known_key_prefix:
        validate_bits(known_key_prefix)
    if not known_plain:
        raise ValueError("Cần ít nhất một bit bản rõ đã biết.")
    if len(known_plain) > len(cipher):
        raise ValueError("Bản rõ đã biết dài hơn bản mã.")
    if len(known_key_prefix) >= KEY_BITS:
        raise ValueError("Phần khóa đã biết phải ngắn hơn 23 bit.")

    stream = [int(b) for b in xor_bits(known_plain, cipher[:len(known_plain)])]
    unknown = KEY_BITS - len(known_key_prefix)
    base = int(known_key_prefix, 2) << unknown if known_key_prefix else 0
    weak = min(weak_check_bits, len(stream))
    total = 1 << unknown

    candidates, weak_matches = [], 0
    step = max(1, total // 20)
    start = time.perf_counter()
    for u in range(total):
        k = base | u
        x, y, z = _key_int_to_regs(k)
        matched = _tiny_bits(x, y, z, stream)
        if matched >= weak:
            weak_matches += 1
            if matched == len(stream):
                candidates.append(f"{k:023b}")
        if progress and u % step == 0:
            progress(u, total)
    seconds = time.perf_counter() - start
    return {
        "keystream": "".join(map(str, stream)),
        "candidates": candidates,
        "tried": total,
        "unknown_bits": unknown,
        "seconds": seconds,
        "keys_per_second": total / seconds if seconds > 0 else float("inf"),
        "weak_bits": weak,
        "weak_matches": weak_matches,
    }


def describe_years(seconds: float) -> str:
    years = seconds / (365.25 * 24 * 3600)
    if years < 1:
        return f"{seconds / 3600:,.1f} giờ"
    return f"{years:,.0f} năm"


def _bits_of(text: str) -> str:
    return "".join(f"{b:08b}" for b in text.encode("utf-8"))


def _text_of(bits: str) -> str:
    return bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8)).decode("utf-8", "replace")


# Dữ liệu mẫu. Bản tin dùng ASCII chỉ để có chuỗi bit dễ đọc;
# đây KHÔNG phải bảng mã 3 bit trong bài giảng.
DEMO_SECRET_KEY = "01101011010011011000101"
DEMO_HEADER = "GSM:"          # phần đầu cố định, kẻ tấn công biết trước (32 bit)
DEMO_BODY = "HEN 9H"          # phần bí mật, kẻ tấn công KHÔNG biết


def run_bruteforce_demo(unknown_bits: int = KEY_BITS) -> dict:
    if type(unknown_bits) is not int or not 1 <= unknown_bits <= KEY_BITS:
        raise ValueError("Số bit khóa chưa biết phải từ 1 đến 23.")

    # ---- Phía người gửi: dùng lõi của Bắp ----
    header, body = _bits_of(DEMO_HEADER), _bits_of(DEMO_BODY)
    cipher, _ = TinyA51(DEMO_SECRET_KEY).encrypt_decrypt(header + body)

    print("\nDEMO TẤN CÔNG VÉT CẠN KHÓA TRÊN TinyA5/1 (biết một phần bản rõ)")
    print("Kẻ tấn công có: bản mã C và phần đầu bản tin đã biết.")
    print(f"Phần đầu đã biết : '{DEMO_HEADER}' = {len(header)} bit")
    print(f"Bản mã C ({len(cipher)} bit): {cipher}")

    prefix = DEMO_SECRET_KEY[:KEY_BITS - unknown_bits]
    if prefix:
        print(f"Chế độ thu nhỏ để kịp giờ: giả định biết {len(prefix)} bit đầu khóa = {prefix}")
    print(f"Không gian cần thử: 2^{unknown_bits} = {1 << unknown_bits:,} khóa ...")

    def show(done, total):
        print(f"\r  đã thử {done / total:5.0%}", end="", flush=True)

    result = brute_force_tiny(header, cipher, prefix, progress=show)
    print("\r  đã thử  100%")
    print(f"S đầu = P đầu XOR C đầu : {result['keystream']}")
    print(f"Thời gian: {result['seconds']:.2f} s  (~{result['keys_per_second']:,.0f} khóa/giây)")
    print(f"Chỉ dùng {result['weak_bits']} bit đã biết -> {result['weak_matches']} khóa cùng khớp "
          "(chưa đủ để chọn đúng khóa).")
    print(f"Dùng đủ {len(header)} bit đã biết -> {len(result['candidates'])} ứng viên:",
          ", ".join(result["candidates"]) or "(không có)")

    # ---- Dùng khóa tìm được để giải mã phần chưa biết, bằng lõi của Bắp ----
    for key in result["candidates"]:
        plain, _ = TinyA51(key).encrypt_decrypt(cipher)
        print(f"Giải mã bằng khóa {key}: '{_text_of(plain)}'")
    found = DEMO_SECRET_KEY in result["candidates"]
    print("Đối chiếu SAU tấn công: khóa thật nằm trong danh sách ứng viên?", found)

    rate = result["keys_per_second"]
    print("\nNgoại suy với tốc độ thử khóa Tiny ở trên (chỉ so sánh độ lớn, không phải đo thực;")
    print("mỗi khóa A5/1 còn tốn 186 nhịp khởi tạo nên con số thật còn lớn hơn):")
    print(f"  Tiny 2^23 khóa : {(1 << 23) / rate:,.1f} giây")
    print(f"  A5/1 2^54 khóa : ~{describe_years((1 << 54) / rate)} (khi 10 bit khóa bị đặt bằng 0)")
    print(f"  A5/1 2^64 khóa : ~{describe_years((1 << 64) / rate)}")
    print("Kết luận: vét cạn phá được Tiny vì khóa quá ngắn. Với A5/1 thật, vét cạn")
    print("trên máy cá nhân không khả thi; các tấn công thực tế dùng cách khác")
    print("(đoán-và-suy ra, đánh đổi thời gian-bộ nhớ) - xem phần phân tích độ an toàn.")
    return result


if __name__ == "__main__":
    run_bruteforce_demo()

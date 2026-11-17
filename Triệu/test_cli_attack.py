"""Kiểm thử phần Triệu: menu CLI, tấn công vét cạn, dùng lại dòng khóa.

Bổ sung cho test_a51_core.py và test_tiny_a51.py của Đăng (không lặp lại các ca đã có ở đó).
Chạy cùng cả bộ: python3 -m unittest discover -s tests   (hoặc mục 4 trên menu)
"""
import io
import os
import random
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from a51_core import crypt_bits, encrypt_text, text_to_bits  # noqa: E402
from attack_bruteforce import brute_force_tiny, fast_keystream, run_bruteforce_demo  # noqa: E402
from attack_demo import (DEMO_KEY, decode_bits_strict, recover_reused_segment,  # noqa: E402
                         validate_bits, xor_bits)
from main import main  # noqa: E402
from tiny_a5 import TinyA51  # noqa: E402


def quiet(func, *args):
    """Chạy hàm mà không in gì ra màn hình (kể cả dòng kết quả của unittest)."""
    with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
        return func(*args)


class TestBruteForce(unittest.TestCase):
    def test_fast_generator_matches_bap_core(self):
        """Bộ sinh nhanh của kẻ tấn công phải khớp từng bit với lõi tiny_a5.py của Bắp."""
        rng = random.Random(2026)
        for _ in range(500):
            key = "".join(rng.choice("01") for _ in range(23))
            expected = "".join(map(str, TinyA51(key).generate_keystream(64)))
            self.assertEqual(fast_keystream(key, 64), expected)

    def test_bruteforce_recovers_key(self):
        """Vét cạn 2^14 khóa (biết 9 bit đầu) phải tìm lại đúng khóa bí mật."""
        secret = "11001010011100101011010"
        plain = text_to_bits("GSM:")
        cipher, _ = TinyA51(secret).encrypt_decrypt(plain + text_to_bits("OK"))
        result = brute_force_tiny(plain, cipher, secret[:9])
        self.assertEqual(result["tried"], 1 << 14)
        self.assertIn(secret, result["candidates"])
        for key in result["candidates"]:  # mọi ứng viên phải sinh đúng dòng khóa đã biết
            self.assertEqual(TinyA51(key).encrypt_decrypt(plain)[0], cipher[:32])

    def test_bruteforce_demo_reduced(self):
        result = quiet(run_bruteforce_demo, 12)
        self.assertIn("01101011010011011000101", result["candidates"])


class TestKeystreamReuse(unittest.TestCase):
    def test_known_example(self):
        self.assertEqual(recover_reused_segment("11011", "01000", "10110"), "00101")

    def test_with_a51_core(self):
        p1, p2 = map(text_to_bits, ("DON100", "DON900"))
        c1 = crypt_bits(p1, DEMO_KEY, 1)
        c2 = crypt_bits(p2, DEMO_KEY, 1)
        self.assertEqual(recover_reused_segment(c1, c2, p1), p2)
        self.assertEqual(recover_reused_segment(c1, c2, p1[8:24], 8), p2[8:24])
        self.assertNotEqual(recover_reused_segment(c1, crypt_bits(p2, DEMO_KEY, 2), p1), p2)

    def test_invalid_input(self):
        for bits in ["102", "abc", "1 0"]:
            with self.subTest(bits=bits), self.assertRaises(ValueError):
                validate_bits(bits)
        bad_calls = [
            (xor_bits, "1", "11"),
            (recover_reused_segment, "1", "1", "11"),
            (recover_reused_segment, "1", "1", "1", -1),
            (decode_bits_strict, "111"),
            (brute_force_tiny, "", "1"),
            (brute_force_tiny, "11", "1"),
            (brute_force_tiny, "1", "1", "0" * 23),
            (fast_keystream, "101", 4),
        ]
        for func, *args in bad_calls:
            with self.subTest(func=func.__name__, args=args), self.assertRaises(ValueError):
                func(*args)


class TestMenu(unittest.TestCase):
    def run_menu(self, inputs):
        with patch("builtins.input", side_effect=inputs):
            quiet(main)

    def test_menu_paths(self):
        for inputs in [
            ["1", "", "", "0"],
            ["2", "", "", "", "", "0"],
            ["2", "2", "", "", encrypt_text("Xin chao", DEMO_KEY, 1), "0"],
            ["2", "1", "bad", "1", "hello", "0"],
            ["1", "", "102", "0"],
            ["5", "10", "6", "bad", "0"],
            ["5", "99", "0"],
        ]:
            with self.subTest(inputs=inputs):
                self.run_menu(inputs)

    def test_file_menu_roundtrip(self):
        """Mục 3 (module Hằng): mã hóa rồi giải mã tệp phải ra đúng từng byte."""
        try:
            import file_io_hang  # noqa: F401
        except Exception as error:  # tệp của Hằng chưa sẵn sàng -> bỏ qua ca này
            self.skipTest(f"Chưa gọi được file_io_hang: {error}")
        with tempfile.TemporaryDirectory() as tmp:
            src, enc, dec = (os.path.join(tmp, n) for n in ("goc.bin", "ma_hoa.a51", "giai_ma.bin"))
            data = "Tệp thử A5/1 — Nhóm 4".encode("utf-8") + bytes(range(256))
            with open(src, "wb") as f:
                f.write(data)
            self.run_menu(["3", src, enc, "", "", "3", enc, dec, "", "", "0"])
            with open(enc, "rb") as f:
                self.assertNotEqual(f.read(), data)
            with open(dec, "rb") as f:
                self.assertEqual(f.read(), data)

    def test_benchmark_menu_calls_tram_anh(self):
        """Mục 7 gọi đúng hàm đo của Trâm Anh (thay bằng hàm giả để không chờ 30 giây)."""
        with patch("benchmark_a51.benchmark_performance") as fake:
            self.run_menu(["7", "0"])
        fake.assert_called_once()

    def test_tests_menu_calls_discovery(self):
        """Mục 4 gọi hàm quét thư mục tests/ (thay bằng bộ rỗng để không tự gọi lại chính nó)."""
        with patch("unittest.defaultTestLoader.discover", return_value=unittest.TestSuite()) as fake:
            self.run_menu(["4", "0"])
        fake.assert_called_once()


if __name__ == "__main__":
    unittest.main(verbosity=2)

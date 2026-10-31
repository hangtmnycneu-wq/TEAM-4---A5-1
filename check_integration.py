"""Kiểm tra tích hợp của Triệu; KHÔNG thay bộ test của Đăng.

Chạy trong thư mục gốc repository (nơi có a51_core.py và core_bap/):
    python3 check_integration.py
"""
import io
import random
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from a51_core import crypt_bits, decrypt_text, encrypt_text, text_to_bits
from attack_bruteforce import brute_force_tiny, fast_keystream, run_bruteforce_demo
from attack_demo import (DEMO_KEY, decode_bits_strict, recover_reused_segment,
                         validate_bits, xor_bits)
from main import main
from team_modules import TinyA51, file_io_problem


def quiet(func, *args):
    with redirect_stdout(io.StringIO()):
        return func(*args)


class IntegrationChecks(unittest.TestCase):
    def test_tiny_examples(self):
        """Hai ví dụ tính tay của Bắp, chạy trên core_bap/tiny_a5 thật."""
        for key, plain, expected, stream in [
            ("10010101001110100110000", "111", "011", "100"),
            ("01101011010011011000101", "101", "000", "101"),
        ]:
            with self.subTest(key=key):
                self.assertEqual(TinyA51(key).encrypt_decrypt(plain), (expected, stream))
                self.assertEqual(TinyA51(key).encrypt_decrypt(expected)[0], plain)

    def test_standard_roundtrip(self):
        for msg in ["", "Xin chao!", "Triệu học thương mại điện tử"]:
            with self.subTest(msg=msg):
                cipher = encrypt_text(msg, DEMO_KEY, 1)
                self.assertEqual(decrypt_text(cipher, DEMO_KEY, 1), msg)
                self.assertEqual(decode_bits_strict(crypt_bits(cipher, DEMO_KEY, 1)), msg)

    def test_fast_generator_matches_bap_core(self):
        """Bộ sinh nhanh của kẻ tấn công phải khớp từng bit với lõi Bắp."""
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

    def test_attack_known_example(self):
        self.assertEqual(recover_reused_segment("11011", "01000", "10110"), "00101")

    def test_attack_real_module(self):
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
        with self.assertRaises(ValueError):
            quiet(run_bruteforce_demo, 0)

    def test_file_io_check_is_reported(self):
        """Chỉ kiểm tra hàm báo trạng thái chạy được; không import file của Hằng ở đây."""
        problem = file_io_problem()
        self.assertTrue(problem is None or "file_io_hang" in problem)

    def test_menu_paths(self):
        sequences = [
            ["1", "", "", "0"],
            ["2", "", "", "", "", "0"],
            ["2", "2", "", "", encrypt_text("Xin chao", DEMO_KEY, 1), "0"],
            ["2", "1", "bad", "1", "hello", "0"],
            ["1", "", "102", "0"],
            ["5", "10", "6", "bad", "0"],
            ["5", "99", "0"],
        ]
        if file_io_problem():  # khi module Hằng chưa an toàn, menu 3 chỉ được báo lý do
            sequences.append(["3", "0"])
        sequences.append(["4", "0"])  # có tests/ thì chạy test Đăng, chưa có thì báo
        for inputs in sequences:
            with self.subTest(inputs=inputs), patch("builtins.input", side_effect=inputs):
                quiet(main)


if __name__ == "__main__":
    unittest.main(verbosity=2)

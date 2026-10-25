"""Kiểm tra tích hợp của Triệu; KHÔNG thay bộ test chuẩn của Đăng."""
import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
from a51_standard import crypt_bits, encrypt_text, decrypt_text, text_to_bits
from tinya51 import TinyA51
from attack_demo import (DEMO_KEY, xor_bits, recover_reused_segment,
                         validate_bits, decode_bits_strict)
from main import main


class IntegrationChecks(unittest.TestCase):
    def test_tiny_examples(self):
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
        with self.assertRaises(ValueError):
            xor_bits("1", "11")
        with self.assertRaises(ValueError):
            recover_reused_segment("1", "1", "11")
        with self.assertRaises(ValueError):
            recover_reused_segment("1", "1", "1", -1)
        with self.assertRaises(ValueError):
            decode_bits_strict("111")

    def test_menu_paths(self):
        sequences = [
            ["1", "", "", "0"],
            ["2", "", "", "", "", "0"],
            ["2", "2", "", "", encrypt_text("Xin chao", DEMO_KEY, 1), "0"],
            ["2", "1", "bad", "1", "hello", "0"],
            ["1", "", "102", "0"],
            ["bad", "3", "4", "5", "0"],
        ]
        for inputs in sequences:
            with self.subTest(inputs=inputs), patch("builtins.input", side_effect=inputs):
                with redirect_stdout(io.StringIO()):
                    main()


if __name__ == "__main__":
    unittest.main(verbosity=2)

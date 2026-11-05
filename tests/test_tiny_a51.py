import unittest

from tiny_a5 import TinyA51


class TestTinyA51(unittest.TestCase):

    # Khóa được lấy từ ví dụ đã sử dụng trong dự án
    KEY = "10010101001110100110000"
    PLAINTEXT = "111"

    def test_valid_key_initialization(self):
        """TC01: Khởi tạo thành công với khóa 23 bit hợp lệ."""
        cipher = TinyA51(self.KEY)

        self.assertEqual(len(cipher.X), 6)
        self.assertEqual(len(cipher.Y), 8)
        self.assertEqual(len(cipher.Z), 9)

    def test_invalid_key_length(self):
        """TC02: Từ chối khóa có độ dài không phải 23 bit."""
        with self.assertRaises(ValueError):
            TinyA51("10101")

    def test_invalid_key_characters(self):
        """TC03: Từ chối khóa chứa ký tự không phải bit."""
        invalid_key = "1001010100111010011000A"

        with self.assertRaises(ValueError):
            TinyA51(invalid_key)

    def test_majority_function(self):
        """TC04: Kiểm tra các trường hợp của hàm Majority."""
        self.assertEqual(TinyA51.majority(0, 0, 0), 0)
        self.assertEqual(TinyA51.majority(1, 0, 0), 0)
        self.assertEqual(TinyA51.majority(1, 1, 0), 1)
        self.assertEqual(TinyA51.majority(1, 1, 1), 1)

    def test_encryption_decryption_consistency(self):
        """TC05: Giải mã phải khôi phục bản rõ ban đầu."""
        encryptor = TinyA51(self.KEY)
        ciphertext, keystream = encryptor.encrypt_decrypt(
            self.PLAINTEXT
        )

        decryptor = TinyA51(self.KEY)
        recovered_plaintext, _ = decryptor.encrypt_decrypt(
            ciphertext
        )

        self.assertEqual(recovered_plaintext, self.PLAINTEXT)
        self.assertEqual(len(keystream), len(self.PLAINTEXT))

    def test_repeatable_keystream(self):
        """TC06: Cùng khóa và trạng thái ban đầu cho cùng keystream."""
        cipher1 = TinyA51(self.KEY)
        cipher2 = TinyA51(self.KEY)

        stream1 = cipher1.generate_keystream(32)
        stream2 = cipher2.generate_keystream(32)

        self.assertEqual(stream1, stream2)
        self.assertEqual(len(stream1), 32)
        self.assertTrue(all(bit in (0, 1) for bit in stream1))

    def test_known_example_output(self):
        """TC07: Kiểm tra đầu ra của ví dụ đã ghi nhận."""

        cipher = TinyA51(self.KEY)

        ciphertext, keystream = cipher.encrypt_decrypt(
            self.PLAINTEXT
        )

        self.assertEqual(keystream, "100")
        self.assertEqual(ciphertext, "011")

if __name__ == "__main__":
    unittest.main()
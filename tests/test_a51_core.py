import unittest

from a51_core import StandardA51, crypt_bits


# Khoa 64 bit dung de kiem thu
KEY = "1101010100111010011000110101010011101001100011010101001110100110"


class TestStandardA51(unittest.TestCase):

    def test_01_encrypt_decrypt_round_trip(self):
        """Ma hoa roi giai ma phai thu lai chuoi bit ban dau."""
        plaintext = "1011001010110101"

        ciphertext = crypt_bits(plaintext, KEY, frame=1)
        decrypted = crypt_bits(ciphertext, KEY, frame=1)

        self.assertEqual(decrypted, plaintext)

    def test_02_different_frames(self):
        """Hai frame khac nhau phai tao ket qua khac nhau voi du lieu nay."""
        plaintext = "1011001010110101"

        ciphertext_1 = crypt_bits(plaintext, KEY, frame=1)
        ciphertext_2 = crypt_bits(plaintext, KEY, frame=2)

        self.assertNotEqual(ciphertext_1, ciphertext_2)

    def test_03_reject_invalid_key_length(self):
        """Khoa khong du 64 bit phai bi tu choi."""
        invalid_key = "0" * 63

        with self.assertRaises(ValueError):
            StandardA51(invalid_key)

    def test_04_reject_invalid_frame(self):
        """Frame am phai bi tu choi."""
        with self.assertRaises(ValueError):
            StandardA51(KEY, frame=-1)
 
    def test_05_standard_a51_test_vector(self):
        """So sanh keystream voi test vector A5/1 tham chieu."""

        # Khoa test vector: 1223456789ABCDEF
        key_bytes = bytes.fromhex("1223456789ABCDEF")

        # Chuyen moi byte sang thu tu bit LSB-first
        vector_key = "".join(
            f"{byte:08b}"[::-1] for byte in key_bytes
        )

        # Frame number cua test vector
        frame = 0x000134

        # Keystream chuan, dong goi thanh byte.
        # 6 bit cuoi duoc dem bang 0.
        expected_hex = "534EAA582FE8151AB6E1855A728C00"

        # Chuyen hex thanh 114 bit dau tien
        expected_bits = "".join(
            f"{byte:08b}"
            for byte in bytes.fromhex(expected_hex)
        )[:114]

        # Tao 114 bit keystream tu chuong trinh cua nhom
        cipher = StandardA51(vector_key, frame)
        actual_bits = "".join(
            str(cipher.next_bit()) for _ in range(114)
        )

        self.assertEqual(actual_bits, expected_bits)

    def test_06_reject_non_binary_key(self):
        """Khoa chua ky tu khong phai 0 hoac 1 phai bi tu choi."""
        invalid_key = "0" * 63 + "A"

        with self.assertRaises(ValueError):
            StandardA51(invalid_key)

    def test_07_reject_frame_out_of_range(self):
        """Frame vuot qua gioi han 22 bit phai bi tu choi."""
        invalid_frame = 2**22

        with self.assertRaises(ValueError):
            StandardA51(KEY, frame=invalid_frame)

if __name__ == "__main__":
    unittest.main(verbosity=2)
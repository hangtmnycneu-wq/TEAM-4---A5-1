import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import a51_core

def key_bytes_to_lsb_first_bits(key_hex: str) -> str:
    """Convert the reference vector's key bytes to the bit order used by this API."""
    raw = bytes.fromhex(key_hex)
    return "".join(str((byte >> bit_index) & 1)
                   for byte in raw for bit_index in range(8))

class TestStandardA51(unittest.TestCase):
    def test_rejects_key_with_wrong_length(self):
        with self.assertRaises(ValueError):
            a51_core.StandardA51("10101")

    def test_rejects_non_binary_key(self):
        with self.assertRaises(ValueError):
            a51_core.StandardA51("0" * 63 + "x")

    def test_rejects_out_of_range_frame(self):
        with self.assertRaises(ValueError):
            a51_core.StandardA51("0" * 64, frame=2**22)

    def test_round_trip_bits(self):
        key = "1101010100111010011000110101010011101001100011010101001110100110"
        plaintext = "0101101011110001"
        ciphertext = a51_core.crypt_bits(plaintext, key, frame=123)
        recovered = a51_core.crypt_bits(ciphertext, key, frame=123)
        self.assertEqual(recovered, plaintext)

    def test_different_frame_changes_stream(self):
        key = "1101010100111010011000110101010011101001100011010101001110100110"
        p = "0" * 128
        self.assertNotEqual(
            a51_core.crypt_bits(p, key, frame=1),
            a51_core.crypt_bits(p, key, frame=2)
        )

    def test_text_round_trip_utf8(self):
        key = "1101010100111010011000110101010011101001100011010101001110100110"
        message = "Xin chào Tiny/A5-1!"
        ciphertext = a51_core.encrypt_text(message, key, frame=1)
        self.assertEqual(a51_core.decrypt_text(ciphertext, key, frame=1), message)

    def test_reference_vector_briceno_frame_count_0x134(self):
        # Reference vector: key 12 23 45 67 89 AB CD EF, COUNT/frame 0x134.
        # Expected A->B stream: 534EAA582FE8151AB6E1855A728C00 (114 meaningful bits;
        # the final 6 bits in the 15th byte are padding zeros).
        key = key_bytes_to_lsb_first_bits("1223456789abcdef")
        cipher = a51_core.StandardA51(key, frame=0x134)
        actual = "".join(str(cipher.next_bit()) for _ in range(114))
        expected = "".join(f"{b:08b}" for b in bytes.fromhex(
            "534eaa582fe8151ab6e1855a728c00"
        ))[:114]
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()

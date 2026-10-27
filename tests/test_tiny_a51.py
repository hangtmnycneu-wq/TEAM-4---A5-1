import importlib.machinery
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TINY_PATH = ROOT / "core_bap" / "tiny_a5"

def load_tiny_class():
    # The current repository stores TinyA5/1 in a file without a .py extension.
    loader = importlib.machinery.SourceFileLoader("tiny_a5_module", str(TINY_PATH))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module.TinyA51

TinyA51 = load_tiny_class()
SLIDE_KEY = "10010101001110100110000"

class TestTinyA51(unittest.TestCase):
    def test_rejects_key_with_wrong_length(self):
        with self.assertRaises(ValueError):
            TinyA51("10101")

    def test_rejects_non_binary_key(self):
        with self.assertRaises(ValueError):
            TinyA51("1001010100111010011000x")

    def test_keystream_and_ciphertext_lengths(self):
        ciphertext, keystream = TinyA51(SLIDE_KEY).encrypt_decrypt("10110")
        self.assertEqual(len(ciphertext), 5)
        self.assertEqual(len(keystream), 5)
        self.assertTrue(set(ciphertext) <= {"0", "1"})
        self.assertTrue(set(keystream) <= {"0", "1"})

    def test_round_trip_with_fresh_instance(self):
        plaintext = "10110"
        ciphertext, _ = TinyA51(SLIDE_KEY).encrypt_decrypt(plaintext)
        recovered, _ = TinyA51(SLIDE_KEY).encrypt_decrypt(ciphertext)
        self.assertEqual(recovered, plaintext)

    def test_deterministic_for_same_key_and_plaintext(self):
        one = TinyA51(SLIDE_KEY).encrypt_decrypt("111")
        two = TinyA51(SLIDE_KEY).encrypt_decrypt("111")
        self.assertEqual(one, two)

    def test_slide_example_expected_output(self):
        # The repository demo comments say P=111 -> C=100 ("D"),
        # which implies S=011. Verify this against the current core.
        ciphertext, keystream = TinyA51(SLIDE_KEY).encrypt_decrypt("111")
        self.assertEqual(keystream, "011")
        self.assertEqual(ciphertext, "100")

    def test_process_bits_api_required_by_demo(self):
        cipher = TinyA51(SLIDE_KEY)
        result = cipher.process_bits("111")
        self.assertEqual(len(result), 3)
        ciphertext, keystream, details = result
        self.assertEqual(len(ciphertext), 3)
        self.assertEqual(len(keystream), 3)
        self.assertEqual(len(details), 3)

if __name__ == "__main__":
    unittest.main()

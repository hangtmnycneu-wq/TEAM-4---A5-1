import unittest

from a51_core import (
    StandardA51,
    encrypt_text,
    decrypt_text
)
from tiny_a5 import TinyA51


KEY = "1101010100111010011000110101010011101001100011010101001110100110"


def title(text):
    print("\n" + "=" * 65)
    print(text.center(65))
    print("=" * 65)


def demo_standard():
    title("1. STANDARD A5/1 - ENCRYPTION / DECRYPTION")

    message = "Xin chao! Day la A5/1 chuan."

    encrypted = encrypt_text(message, KEY, frame=1)
    decrypted = decrypt_text(encrypted, KEY, frame=1)

    print("Original :", message)
    print("Encrypted:", encrypted)
    print("Decrypted:", decrypted)

    passed = decrypted == message
    print("Result   :", "PASSED" if passed else "FAILED")

    return passed


def demo_frame():
    title("2. STANDARD A5/1 - FRAME NUMBER")

    message = "A5/1 DEMO"

    result_1 = encrypt_text(message, KEY, frame=1)
    result_2 = encrypt_text(message, KEY, frame=2)

    print("Frame 1:", result_1)
    print("Frame 2:", result_2)

    passed = result_1 != result_2
    print("Result :", "PASSED" if passed else "FAILED")

    return passed


def demo_tiny():
    title("3. TINY A5/1 - ENCRYPTION / DECRYPTION")

    key = "10110100101101001011010"
    plaintext = "1011001010110101"

    # Khởi tạo riêng cho mỗi lần mã hóa và giải mã
    tiny_encrypt = TinyA51(key)
    ciphertext, keystream = tiny_encrypt.encrypt_decrypt(plaintext)

    tiny_decrypt = TinyA51(key)
    recovered, _ = tiny_decrypt.encrypt_decrypt(ciphertext)

    print("Key       :", key)
    print("Plaintext :", plaintext)
    print("Keystream :", "".join(map(str, keystream)))
    print("Ciphertext:", ciphertext)
    print("Recovered :", recovered)

    passed = recovered == plaintext
    print("Result    :", "PASSED" if passed else "FAILED")

    return passed


def demo_test_vector():
    title("4. STANDARD A5/1 - OFFICIAL TEST VECTOR COMPARISON")

    key_bytes = bytes.fromhex("1223456789ABCDEF")

    # Chuyển khóa sang LSB-first theo từng byte
    vector_key = "".join(
        f"{byte:08b}"[::-1] for byte in key_bytes
    )

    frame = 0x000134

    expected_hex = "534EAA582FE8151AB6E1855A728C00"

    expected_bits = "".join(
        f"{byte:08b}"
        for byte in bytes.fromhex(expected_hex)
    )[:114]

    cipher = StandardA51(vector_key, frame)

    actual_bits = "".join(
        str(cipher.next_bit()) for _ in range(114)
    )

    # Đóng gói 114 bit thành 15 byte, đệm 6 bit cuối bằng 0
    actual_hex = (
        int(actual_bits.ljust(120, "0"), 2)
        .to_bytes(15, "big")
        .hex()
        .upper()
    )

    print("Key          : 1223456789ABCDEF")
    print("Frame Number : 0x000134")
    print("Direction    : A -> B (114 bits)")
    print()
    print("Expected     :", expected_hex)
    print("Actual       :", actual_hex)

    passed = actual_bits == expected_bits

    print()
    print("Comparison   :", "PASSED" if passed else "FAILED")

    return passed


def run_test_suite():
    title("5. AUTOMATED TEST SUITE")

    loader = unittest.TestLoader()
    suite = loader.discover("tests", pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\nTotal tests :", result.testsRun)
    print("Failures    :", len(result.failures))
    print("Errors      :", len(result.errors))

    return result.wasSuccessful()


def main():
    title("A5/1 ENCRYPTION SYSTEM - FULL DEMONSTRATION")

    results = []

    results.append(demo_standard())
    results.append(demo_frame())
    results.append(demo_tiny())
    results.append(demo_test_vector())
    results.append(run_test_suite())

    title("FINAL DEMONSTRATION SUMMARY")

    names = [
        "Standard A5/1",
        "Frame Number",
        "Tiny A5/1",
        "Standard Test Vector",
        "Automated Test Suite"
    ]

    for name, passed in zip(names, results):
        print(f"{name:<30}: {'PASSED' if passed else 'FAILED'}")

    print("\nOVERALL STATUS:",
          "ALL TESTS PASSED" if all(results) else "FAILED")

    print("\nDemo completed.")


if __name__ == "__main__":
    main()
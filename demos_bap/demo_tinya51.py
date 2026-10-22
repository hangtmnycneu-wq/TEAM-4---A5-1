import sys
import os

# Thêm đường dẫn để import module từ thư mục core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.tiny_a51 import TinyA51

def run_demo():
    # Dữ liệu ví dụ chuẩn theo Slide
    K_slide = "10010101001110100110000"
    P_slide = "111"  # Chữ H (3 bit)

    print("==================================================")
    print("  DEMO TRỰC QUAN HÓA TINYA5/1 (BÀI TẬP SLIDE)     ")
    print("==================================================")
    print(f"Khóa K (23 bit): {K_slide}")
    print(f"Bản rõ P       : {P_slide} (Chữ 'H')\n")

    cipher = TinyA51(K_slide)
    c_text, ks_text, details = cipher.process_bits(P_slide)

    for i, step_info in enumerate(details):
        (x1, y3, z3, m, clocked), X, Y, Z, s_i = step_info
        print(f"--- BƯỚC {i} ---")
        print(f"  * Bit kiểm tra : x1={x1}, y3={y3}, z3={z3}")
        print(f"  * Hàm đa số    : m = maj({x1}, {y3}, {z3}) = {m}")
        print(f"  * Thanh ghi quay: {', '.join(clocked)}")
        print(f"  * Trạng thái   : X={''.join(map(str, X))}, Y={''.join(map(str, Y))}, Z={''.join(map(str, Z))}")
        print(f"  * Bit sinh ra  : s_{i} = {s_i}\n")

    print("--------------------------------------------------")
    print(f"Dãy Keystream (S): {ks_text}")
    print(f"Bản mã C = P XOR S: {c_text} (Chữ 'D')")
    print("--------------------------------------------------")

if __name__ == "__main__":
    run_demo()
import a51_core
import os
# Import module A5/1 của Thành viên 1 (Giả sử file của bạn ấy tên là a51_core.py)
# import a51_core 

def process_file_a51(input_file, output_file, key, frame_number):
    """
    Hàm mã hoá/giải mã file sử dụng thuật toán A5/1.
    Vì A5/1 là mã dòng, phép XOR hoạt động hai chiều: chạy hàm này 1 lần là mã hoá, 
    chạy lần 2 với file mã hoá sẽ là giải mã.
    """
    
    # Kiểm tra file đầu vào có tồn tại không
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Không tìm thấy file: {input_file}")

    # 1. Khởi tạo đối tượng A5/1 từ code của Thành viên 1
    # cipher = a51_core.A5_1(key, frame_number) 
    
    print(f"Đang xử lý file: {input_file}...")
    
    # Mở file đầu vào ở chế độ đọc nhị phân (rb) và file đầu ra ở chế độ ghi nhị phân (wb)
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        cipher = a51_core.StandardA51(key, frame_number)
        while True:
            # Đọc từng byte một từ file gốc
            byte_data = f_in.read(1)
            
            if not byte_data:
                break # Đã đọc đến cuối file (EOF)
                
            # Chuyển byte vừa đọc thành số nguyên để thực hiện phép toán bit
            plain_byte = int.from_bytes(byte_data, byteorder='big')
            
            # 2. Sinh 8 bit (1 byte) Keystream từ hệ A5/1
            keystream_byte = 0
            for _ in range(8):
                # Giả định Thành viên 1 viết hàm get_bit() trả về giá trị 0 hoặc 1
                bit = cipher.next_bit() 
                # XÓA DÒNG NÀY VÀ MỞ COMMENT DÒNG TRÊN KHI RÁP CODE
                
                # Dịch trái 1 bit và nối bit mới sinh vào cuối (bitwise OR)
                keystream_byte = (keystream_byte << 1) | bit
                
            # 3. Thực hiện phép mã hoá cốt lõi của hệ mã dòng: Bản rõ XOR Keystream
            cipher_byte = plain_byte ^ keystream_byte
            
            # Ghi byte kết quả ra file mới
            f_out.write(cipher_byte.to_bytes(1, byteorder='big'))

    print(f"Xử lý hoàn tất! File đầu ra lưu tại: {output_file}")

# --- KỊCH BẢN TEST CỦA RIÊNG LEADER ---
if __name__ == "__main__":
    # Test thử file văn bản
    # process_file_a51("test_input.txt", "encrypted.bin", key="khoa_test", frame_number=123)
    
    # Test giải mã lại xem có khôi phục đúng không
    # process_file_a51("encrypted.bin", "decrypted.txt", key="khoa_test", frame_number=123)
    pass
# Tạo biến key_chuan chứa 64 bit trước khi dùng
key_chuan = "1101010100111010011000110101010011101001100011010101001110100110"

# 1. Mã hoá
process_file_a51("test.txt", "test_encrypted.bin", key_chuan, 1)
print("1. Đã mã hoá thành công!")

# 2. Giải mã
process_file_a51("test_encrypted.bin", "test_decrypted.txt", key_chuan, 1)
print("2. Đã giải mã thành công!")
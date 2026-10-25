# Phần tích hợp của Triệu

Bản chạy thử riêng cho bài nhóm ATBMTT. Dùng logic hai lõi Python do Triệu gửi trong cuộc trò chuyện; không lấy trực tiếp mã nguồn từ GitHub. Các chú thích được rút gọn, logic và tên hàm lõi được giữ nguyên. Không thay thế hoặc ghi đè repository của nhóm.

## Các file

| File | Nguồn và vai trò |
|---|---|
| a51_standard.py | Logic của Trâm Anh; bản sao để chạy thử độc lập |
| tinya51.py | Logic của Bắp; bản sao để chạy thử độc lập |
| main.py | Phần Triệu: menu, kiểm tra dữ liệu, gọi module |
| attack_demo.py | Phần Triệu: mô phỏng dùng lại dòng khóa và hàm suy ra bản rõ |
| check_integration.py | Kiểm tra tích hợp, không phải bộ test chuẩn của Đăng |
| README_Trieu.md | Hướng dẫn này |

## Chạy trên máy

Cần Python 3, không cần cài thêm thư viện bằng pip. Giải nén, mở Terminal tại thư mục chứa main.py và chạy:

```bash
python3 main.py
```

Trên macOS, có thể gõ `cd ` (có dấu cách), kéo thư mục trieu_demo từ Finder vào Terminal, nhấn Enter. Sau đó chạy lệnh trên. Gõ `python3 --version` để kiểm tra máy có Python; nếu máy báo thiếu công cụ hoặc yêu cầu cài đặt, xử lý cài Python trước.

Chạy kiểm tra:

```bash
python3 check_integration.py
```

Chạy riêng demo tấn công:

```bash
python3 attack_demo.py
```

## Thử menu theo thứ tự

1. Chọn 1. Nhấn Enter hai lần để dùng khóa và bản rõ mẫu. Kết quả S=100, C=011, giải mã=111. Màn hình in ba vòng của Tiny.
2. Chọn 2. Chọn 1 hoặc Enter để mã hóa. Nhấn Enter cho khóa, frame và bản rõ mẫu. Màn hình cho bản mã dạng bit và bản rõ khôi phục.
3. Chọn 2, sau đó 2 để giải mã riêng. Nhập đúng khóa, frame, rồi dán bản mã dạng bit đã nhận. Giao diện kiểm tra số bit chia hết cho 8 và UTF-8.
4. Chọn 5. Màn hình minh họa khôi phục DON900 khi biết DON100 và hai bản mã dùng chung dòng khóa.
5. Chọn 3 hoặc 4 sẽ thông báo chưa tích hợp Hằng/Đăng. Đây là trạng thái thật, không có chức năng file hoặc test suite giả.
6. Chọn 0 để thoát.

## Phân tích demo tấn công

Người gửi tạo P1=DON100 và P2=DON900, mỗi bản tin 6 byte, rồi mã hóa cùng khóa, frame=1 và cùng vị trí bắt đầu. Mỗi bản tin chỉ cần 48 bit. Hàm recover_reused_segment chỉ nhận C1, C2 và P1 đã biết (cùng offset bit tùy chọn), không nhận khóa hay dòng khóa. Nó tính C1 XOR C2 XOR P1 để khôi phục P2. Sau đó bên điều khiển demo mới đối chiếu với P2 gốc.

Nếu P1 chỉ biết một đoạn thì chỉ khôi phục đoạn P2 tương ứng. Hai bản mã phải căn cùng vị trí dòng khóa. Demo đối chiếu đổi frame bản tin thứ hai thành 2 cho thấy cách suy ra cũ không khôi phục được P2 trong bộ dữ liệu này. Điều này không chứng minh mọi cặp frame luôn tạo bản mã khác nhau cho mọi đoạn ngắn.

## Điều đã kiểm tra và điều chưa kiểm tra

Đã chạy sáu phương thức kiểm tra, có nhiều trường hợp con: hai ví dụ Tiny và giải mã lại; A5/1 khôi phục chuỗi rỗng, ASCII và tiếng Việt; ví dụ tấn công 5 bit; tấn công qua module Trâm Anh gồm đoạn con và frame khác; dữ liệu sai; các luồng menu mã hóa, giải mã, chọn sai và chức năng chờ tích hợp. Tất cả qua khi đóng gói.

Chưa đối chiếu A5/1 với test vector độc lập. Đoạn code Trâm Anh dùng mảng đánh số từ 1; CLK=(9,11,11) và TAPS tương ứng không được tự sửa chỉ vì khác số trong bảng đánh từ 0. Cần Đăng kiểm chứng thứ tự nạp khóa bằng vector ngoài. Khóa được nạp theo đúng thứ tự ký tự chuỗi, frame theo LSB trước như mã được cung cấp.

Module Trâm Anh tiếp tục sinh dòng bit sau khi khởi tạo; chương trình này không bổ sung cơ chế chia file hay chuyển khung GSM. Chức năng chuỗi dài dùng cơ chế liên tục đang có, không nên gọi là mô phỏng đầy đủ lưu lượng GSM. Demo tấn công chọn bản tin ngắn để không cần quyết định lịch nhiều khung.

Giải mã ra UTF-8 hợp lệ không chứng minh khóa đúng hoặc dữ liệu nguyên vẹn: lõi hiện không có xác thực. Khôi phục khớp bản gốc trong kiểm tra chỉ xác nhận các trường hợp thử.

Tiny vẫn cần đối chiếu slide gốc do phần công thức của Hằng và Bắp trong DOCX đang khác nhau.

## Đưa phần Triệu vào repository

Sau khi clone repository, làm trên nhánh riêng của Triệu và kiểm tra cấu trúc thật trước khi chép file. Nếu hai lõi chưa merge vào main, thống nhất với Hằng cách ghép chúng; tạo nhánh từ main không tự lấy code từ nhánh của các bạn.

File của Triệu là main.py, attack_demo.py, check_integration.py và README_Trieu.md. Hai file lõi là bản sao hỗ trợ chạy thử, không tính là công việc tự viết của Triệu; không chép đè bản của tác giả. Nếu tên module Tiny trên GitHub khác tinya51.py hoặc ở thư mục con, sửa import cho phù hợp. Nếu main.py đã tồn tại, tích hợp vào nó sau khi xem nội dung thay vì ghi đè.

Ví dụ luồng terminal sau khi clone và vào thư mục repo; tên nhánh chỉ là đề xuất:

```bash
git switch -c trieu-cli-attack
git status
```

Sau khi chép, chạy thử và xem thay đổi, chọn đúng các file của mình để commit. Chỉ dùng lệnh dưới đây nếu tên và vị trí file đúng trong repo:

```bash
git add main.py attack_demo.py check_integration.py README_Trieu.md
git diff --cached
git commit -m "feat: them CLI va demo dung lai dong khoa"
git push -u origin trieu-cli-attack
```

Tạo Pull Request trên GitHub để nhóm review và ghép. Không cần tạo commit rỗng hoặc chia giả lịch sử cho đủ số lượng. Nếu nhánh đã tồn tại thì chuyển sang nhánh đó, không chạy lại lệnh tạo nhánh cùng tên.

## Nội dung còn bổ sung vào báo cáo

Triệu đã có phần phân tích độ an toàn. Bổ sung mục dùng lại dòng khóa: điều kiện, phép suy ra, kết quả chạy thật, giới hạn và kết luận. Ghi rõ AI hỗ trợ viết menu, mô phỏng tấn công và kiểm tra tích hợp; lõi thuộc phần đóng góp của Trâm Anh và Bắp. Mỗi thành viên phải hiểu phần mã mình nộp.

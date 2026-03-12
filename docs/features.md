# ĐẶC TẢ TÍNH NĂNG HỆ THỐNG AUTORECON-AGENT

Hệ thống được thiết kế dựa trên kiến trúc Multi-Agent, chia làm các module tính năng chính sau:

## 1. Môi trường Thực thi Cô lập (Dockerized Sandbox Execution)
* **Mô tả:** Hệ thống không cho phép AI chạy các lệnh (commands) trực tiếp trên máy chủ gốc (Host OS) để đảm bảo an toàn tuyệt đối. Mọi mã nguồn (Python, Bash) do LLM sinh ra đều được đẩy vào một container Docker (`recon-sandbox`) đã được cấu hình sẵn các công cụ Pentest.
* **Chi tiết kỹ thuật:**
  * Sử dụng thư viện `docker` của Python để khởi tạo, giao tiếp và hủy container tự động.
  * Tích hợp Volume Mounting để ánh xạ thư mục kết quả từ Docker ra máy Host.

## 2. Thu thập Thông tin Thụ động (Passive Reconnaissance)
* **Mô tả:** Khả năng thu thập thông tin tình báo mở (OSINT) mà không cần tương tác trực tiếp với máy chủ của mục tiêu.
* **Chi tiết kỹ thuật:** * Agent sẽ tự động viết các kịch bản (scripts) truy vấn các API công khai (như Whois, Shodan, crt.sh) để tìm kiếm dải IP thật, chứng chỉ SSL bị rò rỉ, và danh sách Subdomains.
  * Dữ liệu trả về sẽ được trích xuất (parse) thành định dạng JSON/Text để chuyển sang bước tiếp theo.

## 3. Rà quét Chủ động Thông minh (Active Attack Surface Mapping)
* **Mô tả:** Khả năng dò thám và lập bản đồ bề mặt tấn công của mục tiêu thông qua các công cụ gửi gói tin trực tiếp.
* **Chi tiết kỹ thuật:**
  * AI Agent phân tích kết quả từ bước Passive, tự động điều chỉnh tham số các công cụ như `Nmap` (để quét Port/Service) và `Gobuster` (để Brute-force thư mục ẩn).
  * Agent có khả năng tự sửa lỗi (Self-correction) nếu script quét bị lỗi cú pháp trong lần chạy đầu tiên.

## 4. Tự động hóa Báo cáo (Automated Security Reporting)
* **Mô tả:** Chuyển đổi dữ liệu log thô kệch và phân mảnh từ các công cụ Pentest thành một báo cáo bảo mật dễ đọc, chuyên nghiệp.
* **Chi tiết kỹ thuật:**
  * `Reporter_Agent` hoạt động như một bộ lọc (Filter) ngôn ngữ tự nhiên. Nó loại bỏ các log "nhiễu" (false positives), phân loại lỗ hổng hoặc rủi ro (Nghiêm trọng, Cao, Trung bình, Thấp) dựa trên các cổng mở và dịch vụ lỗi thời được tìm thấy.
  * Xuất kết quả ra chuẩn Markdown, sẵn sàng để convert sang PDF hoặc nhúng vào giao diện Web.

## 5. Điều phối Đa tác nhân (LLM Orchestration)
* **Mô tả:** Quản lý vòng đời và luồng giao tiếp của các AI Agent thay vì phải lập trình cứng (hard-code) từng bước rẽ nhánh.
* **Chi tiết kỹ thuật:**
  * Sử dụng framework AutoGen với cơ chế `GroupChat`. 
  * Người dùng chỉ cần nhập một Prompt duy nhất: *"Hãy trinh sát mục tiêu X và cho tôi báo cáo"*. Hệ thống sẽ tự động chỉ định ai đi lấy IP, ai đi quét Port, ai chờ lấy dữ liệu để viết báo cáo mà không cần sự can thiệp của con người giữa chừng.
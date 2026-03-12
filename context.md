# Ý TƯỞNG VÀ KIẾN TRÚC ĐỀ TÀI: AUTORECON-AGENT

## 1. Thông tin chung
* **Tên đề tài:** Xây dựng hệ thống AutoRecon-Agent: Thu thập thông tin tình báo website thụ động/chủ động trên môi trường Docker cô lập.
* **Mục tiêu:** Ứng dụng mô hình Multi-Agent (AutoGen) để tự động hóa Phase 1 (Reconnaissance) và Phase 3 (Reporting) trong quy trình Pentest.
* **Giới hạn phạm vi (Scope):** Chỉ tập trung thu thập thông tin và lập báo cáo. Không thực hiện khai thác lỗ hổng (Exploitation) để đảm bảo an toàn và tuân thủ đạo đức bảo mật.

## 2. Công nghệ lõi (Tech Stack)
* **Framework Multi-Agent:** AutoGen (Python).
* **Môi trường thực thi (Sandbox):** Docker Container (Cô lập tiến trình chạy tool mạng, tránh rác OS host).
* **Mô hình LLM:** Groq API / Gemini API (Tốc độ suy luận nhanh, chi phí 0đ cho môi trường phát triển).
* **Mở rộng backend (Tùy chọn):** Quản lý luồng quét và lưu trữ lịch sử báo cáo bằng Java Spring Boot, kết nối qua REST API với service AutoGen Python.

## 3. Kiến trúc các Agent (Tác nhân)

Hệ thống bao gồm 4 Agent chính giao tiếp với nhau qua một Shared Chat (GroupChat):

### 3.1. Orchestrator_UserProxy (Người điều phối & Thực thi)
* **Vai trò:** Không có LLM. Là cầu nối giữa thế giới AI và máy chủ thực.
* **Nhiệm vụ:** Nhận script Python/Bash từ các Agent khác, đưa vào chạy bên trong Docker Container, thu thập kết quả (stdout/stderr) và trả lại vào nhóm chat.

### 3.2. Passive_Recon_Agent (Trinh sát Thụ động)
* **Vai trò:** Chuyên gia OSINT (Open-Source Intelligence).
* **Nhiệm vụ:** Tìm kiếm thông tin rò rỉ trên Internet mà không gửi request trực tiếp đến server mục tiêu.
* **Công cụ sử dụng:** Viết script gọi API Shodan, DNSDumpster, Whois, theHarvester.
* **Đầu ra:** Thông tin chủ sở hữu domain, dải IP, lịch sử DNS, các subdomain bị lộ.

### 3.3. Active_Recon_Agent (Trinh sát Chủ động)
* **Vai trò:** Chuyên gia rà quét mạng.
* **Nhiệm vụ:** Tương tác trực tiếp với mục tiêu để vẽ bản đồ bề mặt tấn công (Attack Surface). Phân tích cấu trúc mạng tiềm năng (như việc mục tiêu có sử dụng Firewall hay nằm trong vùng DMZ hay không dựa trên phản hồi của port).
* **Công cụ sử dụng:** Viết lệnh chạy Nmap (quét port/service), Gobuster/ffuf (brute-force thư mục ẩn).
* **Đầu ra:** Danh sách Port đang mở, dịch vụ đang chạy (phiên bản Nginx/Apache), các API endpoint hoặc thư mục admin bị lộ.

### 3.4. Reporter_Agent (Chuyên gia Báo cáo)
* **Vai trò:** Thư ký tổng hợp.
* **Nhiệm vụ:** Đọc toàn bộ log thô từ 2 Agent trinh sát trên. Lọc bỏ thông tin rác.
* **Đầu ra:** Xuất ra file `report_<target>.md` chuẩn format, phân loại rõ ràng mức độ nghiêm trọng của các thông tin tìm thấy.

## 4. Luồng hoạt động (Workflow)
1. **Khởi tạo:** Người dùng nhập mục tiêu (VD: `example.com`).
2. **Phase 1a (Passive):** `Passive_Recon_Agent` kích hoạt, sinh code tìm IP thực và subdomain -> `UserProxy` chạy code -> Trả kết quả.
3. **Phase 1b (Active):** Dựa trên IP lấy được, `Active_Recon_Agent` sinh lệnh quét Nmap và Gobuster -> `UserProxy` chạy lệnh trong Docker -> Trả kết quả raw logs.
4. **Phase 3 (Report):** Nhận thấy đã đủ dữ liệu trinh sát, `Reporter_Agent` tổng hợp nội dung, format thành file Markdown/PDF.
5. **Kết thúc:** Hệ thống tự động dọn dẹp (kill/remove) Docker container để trả lại tài nguyên.

## 5. Cấu trúc thư mục dự kiến
```text
AutoRecon-Agent/
│
├── docker/
│   ├── Dockerfile         # Image chứa Python, Nmap, Gobuster...
│   └── requirements.txt   # Các thư viện Python cần thiết
│
├── agents/
│   ├── config.py          # Cấu hình API Keys (LLMs)
│   ├── executor.py        # (Mới) Chứa logic kết nối với Docker Containert
│   ├── prompts.py         # (Mới) Sẽ chứa kịch bản (System Message) cho các AI
|   ├── core_agents.py     # (Mới) Nơi khởi tạo các Agent (Recon, Reporter)
|   └── main.py            # Khởi chạy luồng (Entry point), file này sẽ rất ngắn gọn
│
├── workspace/             # Mount volume với Docker để lưu file quét
│   └── reports/           # Nơi chứa file kết quả cuối cùng
│
└── context.md             # File tài liệu dự án này
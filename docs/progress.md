# TIẾN ĐỘ DỰ ÁN: AUTORECON-AGENT

## Phase 1: Khởi tạo & Môi trường nền tảng (Foundation)
- [x] Cài đặt cấu hình WSL 2 và Docker Desktop trên Windows.
- [x] Thiết lập cấu trúc thư mục dự án (`docker/`, `agents/`, `workspace/`, `docs/`).
- [x] Xây dựng file `Dockerfile` chuẩn chứa công cụ mạng (Nmap, Gobuster, Python).
- [x] Build thành công Docker image `recon-sandbox`.
- [x] Tạo môi trường ảo (venv) và cài đặt thư viện (`pyautogen`, `docker`, `python-dotenv`).
- [x] Cấu hình file `.env` và `config.py` để kết nối API của LLM (Groq/Gemini).

## Phase 2: Phát triển Tác nhân cốt lõi (Core Agents)
- [x] Xây dựng `UserProxy Agent`: Cấu hình executor để truyền code/script vào chạy trong Docker container.
- [ ] Xây dựng `Passive_Recon_Agent`: Định nghĩa System Prompt và cung cấp tool/script gọi API OSINT (theHarvester, Shodan, DNSDumpster).
- [ ] Xây dựng `Active_Recon_Agent`: Định nghĩa System Prompt và viết logic để Agent tự sinh lệnh Nmap, Dirb/Gobuster.
- [ ] Xây dựng `Reporter_Agent`: Định nghĩa System Prompt và tạo Template Báo cáo (Markdown/PDF) để Agent điền dữ liệu.

## Phase 3: Tích hợp Luồng làm việc (Workflow & Orchestration)
- [ ] Thiết lập `GroupChat` và `GroupChatManager` để các Agent giao tiếp.
- [ ] Cấu hình điều kiện chuyển trạng thái (State Transition): Bắt buộc Recon quét xong mới gọi Reporter.
- [ ] Viết hàm (function) để lưu file log raw từ Docker xuống thư mục `workspace/`.
- [ ] Viết hàm (function) để đọc file log trả lại làm context cho Reporter Agent.

## Phase 4: Kiểm thử và Tối ưu (Testing & Refinement)
- [ ] Chạy thử nghiệm quy trình Passive Recon với một domain public (ví dụ: `scanme.nmap.org`).
- [ ] Chạy thử nghiệm Active Recon nhắm vào các container nội bộ đã có sẵn (ví dụ: `juice-shop`, `webgoat`).
- [ ] Tối ưu hóa System Prompts để giảm thiểu tình trạng AI "ảo giác" (hallucination) sinh code sai.
- [ ] Xử lý lỗi (Error handling) khi tool chạy trong Docker bị time-out hoặc crash.

## Phase 5: Mở rộng & Đóng gói (Tùy chọn cho điểm cộng)
- [ ] Đóng gói toàn bộ luồng AutoGen thành các hàm chuẩn (Modularization).
- [ ] (Tùy chọn) Viết backend REST API bằng Java Spring Boot để quản lý các luồng quét từ xa.
- [ ] Hoàn thiện báo cáo đồ án (Vẽ Sequence Diagram, Architecture Diagram).
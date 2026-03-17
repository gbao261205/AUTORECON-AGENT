# THÔNG TIN BÀN GIAO DỰ ÁN (PROJECT HANDOVER CONTEXT)

## 1. Tổng quan dự án (Project Overview)
* **Tên dự án:** AutoRecon-Agent
* **Mục tiêu:** Xây dựng hệ thống Multi-Agent (dùng AutoGen) để tự động hóa quy trình Pentest Website: Phase 1 (Reconnaissance) và Phase 3 (Reporting).
* **Kiến trúc lõi:** AutoGen (Python) kết hợp Docker (Ubuntu Sandbox) chạy trên môi trường Windows WSL2.

## 2. Trạng thái hiện tại (Current State) - ĐÃ HOÀN THÀNH
Hệ thống lõi đã hoạt động thành công quy trình GroupChat khép kín. Cụ thể:
1. **Môi trường:** Đã build xong Docker image `recon-sandbox` chứa Nmap, Python3, Gobuster...
2. **Cấu trúc source code:**
   * `.env` & `agents/config.py`: Quản lý API Key (Groq/Gemini).
   * `agents/executor.py`: Cấu hình `DockerCommandLineCodeExecutor` map volume với thư mục `workspace/` và set timeout = 300s.
   * `agents/core_agents.py`: Khởi tạo 4 Agent (UserProxy, Passive_Recon, Active_Recon, Reporter).
   * `agents/main.py`: Thiết lập `GroupChat` và `GroupChatManager` để điều phối luồng làm việc tự động.
   * `agents/prompts.py`: Chứa System Prompts bằng **Tiếng Anh chuyên ngành**, cấu hình quy tắc Turn-based (đợi tín hiệu `DONE_PASSIVE`, `DONE_ACTIVE` mới được chạy).

## 3. Các bài học/Lỗi đã khắc phục (Resolved Issues - DO NOT REPEAT)
* **Lỗi môi trường Python:** Trong Docker Ubuntu, AI từng gọi lệnh `python` gây lỗi "not found". Đã fix cứng trong Prompt: Bắt buộc dùng `python3`.
* **Lỗi Nmap Timeout:** AI từng dùng lệnh Nmap quét quá sâu (`-sV -O`) gây timeout. Đã fix cứng trong Prompt: Bắt buộc dùng cờ quét nhanh (`-Pn -F -sV`).
* **Lỗi AI tự biên tự diễn:** `Reporter_Agent` từng tự sinh code bash để chạy lại công cụ. Đã fix bằng lệnh cấm tuyệt đối sinh code trong Prompt của Reporter.
* **Lỗi ngắt kết nối sớm:** Cấu hình `is_termination_msg` của UserProxy đã được đổi thành nhận diện chữ `TERMINATE`. Các Agent chỉ được nói `TERMINATE` ở bước cuối cùng của báo cáo.

## 4. Nhiệm vụ tiếp theo (Next Steps / To-Do)
* **Nhiệm vụ 1 (Tối ưu file Output):** Hiện tại log đang in hết lên terminal. Cần viết thêm logic để `UserProxy` (hoặc `Reporter_Agent`) lưu bản báo cáo Markdown cuối cùng thành một file vật lý (VD: `workspace/report_scanme_nmap_org.md`).
* **Nhiệm vụ 2 (Local Testing):** Chuyển mục tiêu từ public (`scanme.nmap.org`) sang quét các mục tiêu local an toàn đã có sẵn trong Docker của hệ thống (như container `juice-shop` hoặc `webgoat`).
* **Nhiệm vụ 3 (Error Handling):** Xử lý ngoại lệ trong Python code ở `main.py` để phòng trường hợp API LLM bị lỗi mạng hoặc quá tải (Rate limit).
* **Nhiệm vụ 4 (Tùy chọn Mở rộng):** (Dành cho việc nâng cấp) Viết một backend nhỏ hoặc script tích hợp luồng quét này vào giao diện người dùng.
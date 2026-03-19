# File: agents/main.py
import os
import re
from datetime import datetime
from autogen import GroupChat, GroupChatManager
from agents.core_agents import (
    create_user_proxy,
    create_passive_recon_agent,
    create_active_recon_agent,
    create_reporter_agent
)
from agents.config import default_llm_config

def run_pentest_workflow(target_domain: str):
    print(f"[*] Đang khởi tạo đội ngũ Multi-Agent nhắm mục tiêu: {target_domain}...\n")
    
    user_proxy = create_user_proxy()
    passive_agent = create_passive_recon_agent()
    active_agent = create_active_recon_agent()
    reporter_agent = create_reporter_agent()

    agents_list = [user_proxy, passive_agent, active_agent, reporter_agent]
    
    groupchat = GroupChat(
        agents=agents_list,
        messages=[],
        max_round=15,
        speaker_selection_method="auto"
    )

    manager = GroupChatManager(
        groupchat=groupchat,
        llm_config=default_llm_config
    )

    print("[*] Bắt đầu luồng kiểm thử Phase 1 & 3...")
    
    initial_message = f"""
    Mục tiêu Pentest (Phase 1 & 3) của chúng ta hôm nay là: {target_domain}.
    
    - Passive_Recon_Agent hãy bắt đầu trước. Thu thập thông tin IP và Subdomain.
    - UserProxy sẽ chạy code giúp các bạn.
    - Khi Passive xong, Active_Recon_Agent hãy quét Nmap vào IP tìm được.
    - Cuối cùng, Reporter_Agent hãy tổng hợp thành file Markdown.
    """
    
    # 1. Chạy luồng chat và HỨNG KẾT QUẢ VÀO BIẾN chat_result
    chat_result = user_proxy.initiate_chat(
        manager,
        message=initial_message
    )

    # ==========================================
    # NHIỆM VỤ 1: TỐI ƯU FILE OUTPUT
    # ==========================================
    print("\n[*] Đang trích xuất báo cáo và lưu ra file vật lý...")
    
    report_content = ""
    # Duyệt ngược lịch sử chat để tìm tin nhắn cuối cùng của Reporter_Agent
    for msg in reversed(chat_result.chat_history):
        if msg.get("name") == "Reporter_Agent" and "TERMINATE" in msg.get("content", ""):
            raw_content = msg.get("content").replace("TERMINATE", "").strip()
            
            # Ưu tiên lấy từ đúng đầu dòng Tiêu đề Report (Chống AI luyên thuyên viết văn bên trên)
            if "# SECURITY" in raw_content.upper():
                start_idx = raw_content.upper().find("# SECURITY")
                report_content = raw_content[start_idx:].strip()
                # Xóa dấu code block dư thừa ở cuối nếu AI bọc Report trong khung markdown
                if report_content.endswith("```"):
                    report_content = report_content[:-3].strip()
            else:
                # Nếu AI quên viết tiêu đề, thử tìm trong khung code Markdown khép kín
                match_md = re.search(r'```markdown\n(.*?)\n```', raw_content, re.IGNORECASE | re.DOTALL)
                if match_md:
                    report_content = match_md.group(1).strip()
                else:
                    report_content = raw_content
                
            break
            
    if report_content:
        # Lấy đường dẫn tuyệt đối của thư mục workspace
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        workspace_dir = os.path.join(base_dir, "workspace", "reports")
        os.makedirs(workspace_dir, exist_ok=True)
        
        # Đặt tên file có chứa thời gian quét để không bị ghi đè
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_domain = target_domain.replace('.', '_')
        filename = f"pentest_report_{safe_domain}_{timestamp}.md"
        filepath = os.path.join(workspace_dir, filename)
        
        # Ghi nội dung ra file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(report_content)
            
        print(f"\n[+] TUYỆT VỜI! Đã lưu báo cáo thành công tại: {filepath}")
    else:
        print("\n[-] Lỗi: Không tìm thấy nội dung báo cáo từ Reporter_Agent trong lịch sử chat.")

if __name__ == "__main__":
    TARGET = "scanme.nmap.org"
    run_pentest_workflow(TARGET)
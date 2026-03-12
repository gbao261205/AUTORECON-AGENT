# File: agents/main.py
from autogen import AssistantAgent
from agents.config import default_llm_config
from agents.core_agents import create_user_proxy

def test_docker_and_llm():
    print("[*] Đang khởi tạo UserProxy (Docker Sandbox)...")
    user_proxy = create_user_proxy()

    print("[*] Đang khởi tạo Test Agent...")
    
    test_agent = AssistantAgent(
        name="Test_Recon_Agent",
        llm_config=default_llm_config,
        system_message="""Bạn là một chuyên gia mạng.
        Nhiệm vụ của bạn là viết script bash (bọc trong ```bash và ```) để chạy lệnh nmap quét 2 port 80 và 443 của mục tiêu.
        
        QUY TẮC BẮT BUỘC: 
        1. Lần trả lời đầu tiên: CHỈ ĐƯỢC cung cấp code block, tuyệt đối KHÔNG chứa từ 'TERMINATE'.
        2. Sau đó, UserProxy sẽ tự động chạy code của bạn và gửi lại kết quả nmap thực tế.
        3. Chỉ sau khi bạn đọc được kết quả trả về từ UserProxy, bạn mới tóm tắt kết quả đó và in ra chữ 'TERMINATE' để kết thúc luồng.""",
    )

    print("[*] Bắt đầu luồng kiểm thử...")
    user_proxy.initiate_chat(
        test_agent,
        message="Hãy viết script quét mục tiêu scanme.nmap.org giúp tôi.",
        summary_method="reflection_with_llm",
    )

if __name__ == "__main__":
    test_docker_and_llm()
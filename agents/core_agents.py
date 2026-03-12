#Định nghĩa UserProxy - đại diện thực thi lệnh
from autogen import ConversableAgent
from agents.executor import get_docker_executor

def create_user_proxy():
    """
    Tạo UserProxy Agent. Agent này KHÔNG dùng LLM để suy nghĩ.
    Nhiệm vụ duy nhất của nó là nhận script (bash/python) từ các Agent khác
    và ném vào Docker để chạy.
    """
    # Lấy executor từ file executor.py
    docker_executor = get_docker_executor()

    user_proxy = ConversableAgent(
        name="UserProxy",
        llm_config=False,  # Không cần API Key cho tác nhân này
        human_input_mode="NEVER", # Tự động chạy code mà không cần người dùng gõ 'y' xác nhận
        code_execution_config={"executor": docker_executor},
        is_termination_msg=lambda msg: "TERMINATE" in msg.get("content", "").upper(),
    )
    
    return user_proxy
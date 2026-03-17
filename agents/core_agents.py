# File: agents/core_agents.py
from autogen import ConversableAgent, AssistantAgent
from agents.executor import get_docker_executor
from agents.config import default_llm_config
from agents.prompts import PASSIVE_RECON_PROMPT, ACTIVE_RECON_PROMPT, REPORTER_PROMPT

def create_user_proxy():
    """Tạo UserProxy Agent - Quản lý Docker Sandbox"""
    docker_executor = get_docker_executor()
    user_proxy = ConversableAgent(
        name="UserProxy",
        llm_config=False,
        human_input_mode="NEVER",
        code_execution_config={"executor": docker_executor},
        # Đổi điều kiện kết thúc: Hễ thấy TERMINATE là dừng luồng chat
        is_termination_msg=lambda msg: "TERMINATE" in msg.get("content", "").upper(),
    )
    return user_proxy

def create_passive_recon_agent():
    """Tạo Chuyên gia Trinh sát Thụ động"""
    return AssistantAgent(
        name="Passive_Recon_Agent",
        llm_config=default_llm_config,
        system_message=PASSIVE_RECON_PROMPT,
    )

def create_active_recon_agent():
    """Tạo Chuyên gia Trinh sát Chủ động"""
    return AssistantAgent(
        name="Active_Recon_Agent",
        llm_config=default_llm_config,
        system_message=ACTIVE_RECON_PROMPT,
    )

def create_reporter_agent():
    """Tạo Chuyên gia Báo cáo"""
    return AssistantAgent(
        name="Reporter_Agent",
        llm_config=default_llm_config,
        system_message=REPORTER_PROMPT,
    )
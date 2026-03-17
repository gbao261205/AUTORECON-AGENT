# File: agents/config.py
import os
from dotenv import load_dotenv

# Load các biến môi trường từ file .env
load_dotenv()

# Cấu hình danh sách các Model (LLM) cho AutoGen
# Bạn có thể ưu tiên dùng llama3 hoặc mixtral trên Groq vì nó rất nhanh và miễn phí
llm_config_groq = {
    "config_list": [
        {
            "model": "llama-3.1-8b-instant", 
            "api_key": os.environ.get("GROQ_API_KEY"),
            "api_type": "groq",
        }
    ],
    "temperature": 0.2, # Để temperature thấp để Agent trả lời mang tính kỹ thuật, bớt "ảo giác"
}

llm_config_gemini = {
    "config_list": [
        {
            "model": "gemini-2.5-flash", 
            "api_key": os.environ.get("GEMINI_API_KEY"),
            "api_type": "google",
        }
    ],
    "temperature": 0.2,
}

# Chọn cấu hình mặc định muốn dùng (ở đây ví dụ dùng Groq)
default_llm_config = llm_config_groq
# default_llm_config = llm_config_gemini
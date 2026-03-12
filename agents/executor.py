#Sử dụng module autogen.coding để thực thi code trong Docker, giúp cô lập môi trường và tránh ảnh hưởng đến hệ thống chính
import os
from autogen.coding.docker_commandline_code_executor import DockerCommandLineCodeExecutor

def get_docker_executor():
    """
    Hàm này khởi tạo môi trường thực thi code bên trong Docker.
    Nó sẽ mount thư mục 'workspace' của máy thật vào container
    để các file log quét mạng được lưu lại.
    """
    # Lấy đường dẫn tuyệt đối của thư mục workspace (nằm ngoài thư mục agents)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    workspace_dir = os.path.join(base_dir, "workspace")
    
    # Tạo thư mục nếu nó chưa tồn tại
    os.makedirs(workspace_dir, exist_ok=True)

    print(f"[*] Đang khởi tạo Docker Executor. Thư mục làm việc: {workspace_dir}")

    # Khởi tạo executor với image bạn đã build
    executor = DockerCommandLineCodeExecutor(
        image="recon-sandbox",  # Tên image chúng ta đã build ở bước trước
        timeout=120,            # Thời gian chạy tối đa cho 1 lệnh (Nmap có thể mất thời gian)
        work_dir=workspace_dir  # Mount thư mục workspace vào Docker
    )
    
    return executor
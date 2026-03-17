# Sử dụng base image Ubuntu siêu nhẹ
FROM ubuntu:22.04

# Tránh các prompt hỏi Yes/No khi cài đặt gói
ENV DEBIAN_FRONTEND=noninteractive

# Cập nhật hệ thống và cài đặt các công cụ Recon cơ bản
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    nmap \
    dnsutils \
    whois \
    curl \
    wget \
    iputils-ping \
    dirb \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt một số thư viện Python hỗ trợ mạng (nếu Agent cần viết script)
RUN pip3 install requests scapy bs4

# Thiết lập thư mục làm việc mặc định trong container
WORKDIR /workspace

# Container sẽ giữ trạng thái chạy ngầm để AutoGen có thể gửi lệnh vào
CMD ["tail", "-f", "/dev/null"]
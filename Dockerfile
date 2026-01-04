# 使用轻量级镜像
FROM python:3.9-slim

# 设置版本标签
LABEL version="1.0"

# 安装 requests 库
RUN pip install --no-cache-dir requests

# 设置工作目录
WORKDIR /app

# 复制脚本
COPY reboot_asus.py .

# 设置默认环境变量（可在启动时覆盖）
ENV ROUTER_URL="192.168.50.1"
ENV ROUTER_USER="admin"
ENV ROUTER_PASSWORD=""

# 执行脚本
CMD ["python", "reboot_asus.py"]
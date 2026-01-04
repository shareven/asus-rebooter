# 使用轻量级镜像
FROM python:3.9-slim

# 安装依赖
RUN pip install --no-cache-dir requests

# 设置工作目录
WORKDIR /app

# 复制重启脚本
COPY reboot_asus.py .

# 设置非敏感默认变量
ENV ROUTER_URL="192.168.50.1"
ENV ROUTER_USER="admin"

# 执行脚本
CMD ["python", "reboot_asus.py"]

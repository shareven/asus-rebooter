# ASUS Router Rebooter

[English](README.en.md) | [中文](README.md)

一个轻量级的Python工具，用于远程手动重启华硕（ASUS）路由器，特别适合部署在NAS上，只需在NAS的UI界面启动一次容器即可完成重启操作，容器执行后自动退出。

## 🚀 功能特性

- 自动登录华硕路由器管理界面并执行重启操作
- 特别适合部署在NAS设备上进行远程控制
- 轻量无依赖（仅使用 `requests`）
- 支持 Docker 容器化运行
- 配置灵活，可通过环境变量覆盖默认设置
- 容器运行后自动退出，无需手动管理

## 📋 环境要求

- Docker
- 网络能够访问路由器管理界面

## 🌐 项目地址

项目源码：[https://github.com/shareven/asus-rebooter](https://github.com/shareven/asus-rebooter)

## 🛠️ 使用方法

### 方法一：使用 Docker（通过NAS UI界面）

#### 在NAS UI界面创建和运行容器
1. 在NAS的Docker管理界面中，选择"创建容器"或类似选项
2. 镜像选择：`shareven/asus-rebooter:latest`
3. 在环境变量部分添加以下配置：
   - `ROUTER_URL` = `192.168.50.1` (替换为您的路由器IP)
   - `ROUTER_USER` = `admin` (替换为您的路由器用户名)
   - `ROUTER_PASSWORD` = `your_password` (替换为您的路由器密码)
4. 网络设置选择"Host"模式
5. 启动容器，容器会在重启路由器后自动退出

> 注意：容器会在发送重启命令后自动退出，这是正常行为。

#### 命令行方式（可选）
如果您需要通过命令行运行：
```bash
docker run --network host \
  -e ROUTER_URL=192.168.50.1 \
  -e ROUTER_USER=admin \
  -e ROUTER_PASSWORD=your_password \
  shareven/asus-rebooter:latest
```

### 方法二：使用 Docker Compose（通过NAS UI界面）

许多NAS系统支持Docker Compose（如群晖的"创成式应用程序"功能）：

创建一个 `docker-compose.yml` 文件：

```yaml
version: '3.8'

services:
  asus-rebooter:
    image: shareven/asus-rebooter:latest
    container_name: asus-rebooter
    network_mode: host  # 使用 host 网络模式
    environment:
      - ROUTER_URL=192.168.50.1
      - ROUTER_USER=admin
      - ROUTER_PASSWORD=your_password
    restart: no  # 执行一次后不重启
```

在NAS的Docker Compose功能中使用此配置文件，启动后容器会自动执行重启任务并退出。

### 方法三：作为定时任务（可选）

如果您确实需要定时重启功能（例如在路由器自身定时重启功能不可用时），可以在NAS的Docker管理界面中创建计划任务。

## ⚙️ 配置说明

### 环境变量

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| ROUTER_URL | 192.168.50.1 | 路由器管理界面的IP地址或域名 |
| ROUTER_USER | admin | 路由器登录用户名 |
| ROUTER_PASSWORD | password | 路由器登录密码 |

### Docker 网络配置

使用 Host 网络模式可以让容器直接使用主机的网络栈，这种方式有以下优势：
- 避免了网络地址转换（NAT）的额外开销
- 确保容器能够直接访问路由器的IP地址
- 减少网络延迟，提高连接稳定性

## 🔧 工作原理

1. 程序从环境变量中读取路由器配置信息
2. 使用基本认证（Basic Auth）向路由器管理界面发送认证请求
3. 向 `/apply.cgi` 端点发送重启指令
4. 路由器收到重启指令后会立即断开网络连接，开始重启过程
5. 容器在发送重启指令后自动退出，无需手动管理

## ⚠️ 注意事项

- 使用 Host 网络模式时，容器将直接使用主机网络，确保主机网络能够访问路由器
- 容器在发送重启指令后会自动退出，这是正常行为，表示任务已成功完成
- 请确保网络能够访问路由器管理界面
- 为避免在路由器重启过程中出现网络异常，请确保操作完成后网络会自动恢复
- 不要在路由器正在处理重要任务时执行重启操作
- 请妥善保管路由器的登录凭证，避免安全风险
- 路由器重启过程中，网络连接会中断，确保在合适的时间执行重启操作
- 此工具主要用于NAS远程手动重启，如果路由器已有定时重启功能，建议优先使用路由器内置功能

## 🐛 已知问题

- 未提供错误重试机制
- 未处理登录失败、会话过期等异常情况
- 未验证 CSRF 或登录挑战机制（部分 ASUS 路由器可能启用）

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来帮助改进这个项目。
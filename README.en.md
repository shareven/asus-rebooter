# ASUS Router Rebooter

[English](README.en.md) | [中文](README.md)

A lightweight Python tool for remotely restarting ASUS routers, particularly suitable for deployment on NAS devices. Simply start the container from the NAS UI once to complete the restart operation. The container automatically exits after execution.

## 🚀 Features

- Automatically logs into the ASUS router management interface and performs a restart
- Specifically designed for remote control on NAS devices
- Lightweight with no dependencies (only uses `requests`)
- Supports Docker containerization
- Flexible configuration via environment variables
- Container automatically exits after execution, no manual management required

## 📋 Requirements

- Docker
- Network access to the router management interface

## 🛠️ Usage

### Method 1: Using Docker (via NAS UI)

#### Creating and running the container in the NAS UI
1. In the Docker management interface of your NAS, select "Create Container" or similar option
2. Image selection: `shareven/asus-rebooter:latest`
3. Add the following configurations in the environment variables section:
   - `ROUTER_URL` = `192.168.50.1` (replace with your router IP)
   - `ROUTER_USER` = `admin` (replace with your router username)
   - `ROUTER_PASSWORD` = `your_password` (replace with your router password)
4. Set network mode to "Host"
5. Start the container; it will automatically restart the router and then exit

> Note: The container will automatically exit after sending the restart command, which is normal behavior.

#### Command line method (optional)
If you need to run via command line:
```bash
docker run --network host \
  -e ROUTER_URL=192.168.50.1 \
  -e ROUTER_USER=admin \
  -e ROUTER_PASSWORD=your_password \
  shareven/asus-rebooter:latest
```

### Method 2: Using Docker Compose (via NAS UI)

Many NAS systems support Docker Compose (such as Synology's "Create Application" feature):

Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  asus-rebooter:
    image: shareven/asus-rebooter:latest
    container_name: asus-rebooter
    network_mode: host  # Use host network mode
    environment:
      - ROUTER_URL=192.168.50.1
      - ROUTER_USER=admin
      - ROUTER_PASSWORD=your_password
    restart: no  # Do not restart after completion
```

Use this configuration file in your NAS Docker Compose feature. After starting, the container will automatically execute the restart task and exit.

### Method 3: As a scheduled task (optional)

If you do need scheduled restart functionality (for example when the router's own scheduled restart feature is unavailable), you can create scheduled tasks in your NAS Docker management interface.

## ⚙️ Configuration

### Environment Variables

| Environment Variable | Default Value | Description |
|---------------------|---------------|-------------|
| ROUTER_URL | 192.168.50.1 | Router management interface IP address or domain |
| ROUTER_USER | admin | Router login username |
| ROUTER_PASSWORD | password | Router login password |

### Docker Network Configuration

Using Host network mode allows the container to directly use the host's network stack. This approach has the following advantages:
- Avoids overhead from network address translation (NAT)
- Ensures the container can directly access the router's IP address
- Reduces network latency and improves connection stability

## 🔧 How It Works

1. The program reads router configuration information from environment variables
2. Sends authentication request to router management interface using Basic Auth
3. Sends restart command to `/apply.cgi` endpoint
4. After receiving the restart command, the router immediately disconnects the network and begins the restart process
5. The container automatically exits after sending the restart command, no manual management required

## ⚠️ Notes

- When using Host network mode, the container directly uses the host network; ensure the host network can access the router
- The container will automatically exit after sending the restart command, which is normal behavior indicating the task has been completed successfully
- Ensure network access to the router management interface
- Ensure the network will automatically recover after the restart operation
- Do not perform restart operations while the router is processing important tasks
- Safeguard router login credentials to avoid security risks
- During router restart, network connections will be interrupted; ensure restarts are performed at appropriate times
- This tool is primarily for remote manual restarts on NAS. If your router already has scheduled restart functionality, it's recommended to use the router's built-in feature

## 🐛 Known Issues

- No error retry mechanism provided
- Does not handle login failures, session expiration, or other exceptional situations
- Does not verify CSRF or login challenge mechanisms (some ASUS routers may have these enabled)

## 🤝 Contributing

Feel free to submit Issues and Pull Requests to help improve this project.

## 🌐 Project Address

Source code: [https://github.com/shareven/asus-rebooter](https://github.com/shareven/asus-rebooter)
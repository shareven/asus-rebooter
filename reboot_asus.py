import os
import requests
import base64
import sys

# 获取环境变量 | Get environment variables
router_ip = os.getenv("ROUTER_URL", "192.168.50.1").replace("http://", "").replace("https://", "")
router_account = os.getenv("ROUTER_USER", "admin")
router_password = os.getenv("ROUTER_PASSWORD", "password")

def restart_asus_router():
    if not router_password:
        print("❌ 错误: 未设置 ROUTER_PASSWORD | Error: ROUTER_PASSWORD not set")
        sys.exit(1)

    session = requests.Session()
    base_url = f"http://{router_ip}"
    
    # 核心：生成认证信息 | Core: Generate login_authorization (username:password Base64)
    auth_str = f"{router_account}:{router_password}"
    auth_base64 = base64.b64encode(auth_str.encode()).decode()

    # 匹配华硕 POST 数据结构 | Match ASUS POST data structure
    login_payload = {
        'group_id': '',
        'action_mode': '',
        'action_script': '',
        'action_wait': '5',
        'current_page': 'Main_Login.asp',
        'next_page': 'index.asp',
        'login_authorization': auth_base64,
        'login_captcha': ''  # 即使为空也必须包含 | Must be included even if empty
    }

    headers = {
        "Referer": f"{base_url}/Main_Login.asp",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": base_url
    }

    try:
        print(f"🔑 正在尝试登录 | Attempting to login (Auth: {auth_base64})...")
        
        # 1. 登录认证 | Login authentication
        res = session.post(f'{base_url}/login.cgi', data=login_payload, headers=headers, timeout=10)
        
        cookies = session.cookies.get_dict()
        print(f"📡 响应状态码 | Status Code: {res.status_code}")
        print(f"🍪 实时获取的 Cookies | Cookies: {cookies}")

        # 检查是否成功获取 Session Cookie | Check if Session Cookie was obtained
        if not cookies:
            print("❌ 登录失败：未获取到 Cookie | Login failed: No cookies obtained")
            print("💡 请检查：1.用户名密码 2.验证码 3.是否需要 https | Please check: 1.Auth 2.Captcha 3.Https")
            sys.exit(1)

        print("✅ 登录成功，正在发送重启指令... | Login successful, sending reboot command...")

        # 2. 发送重启指令 | Send reboot command
        reboot_payload = {
            'action_mode': 'reboot',
            'action_script': '',
            'action_wait': '70'
        }
        
        # 必须要 Referer 防止 CSRF | Referer required to prevent CSRF
        headers["Referer"] = f"{base_url}/index.asp"
        
        try:
            session.post(f'{base_url}/apply.cgi', data=reboot_payload, headers=headers, timeout=5)
            print("✅ 重启指令已发送！ | Reboot command sent successfully!")
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
            print("✅ 网络已断开，路由器正在重启... | Connection lost, router is rebooting...")
        
        sys.exit(0)

    except Exception as e:
        print(f"💥 运行异常 | Execution Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    restart_asus_router()

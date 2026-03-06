# 文件: tools/get_tms_cookie.py
# 作者: Claude Code
# 创建日期: 2026/03/06
# 描述: 自动登录TMS系统获取Cookie

import requests
import json
import os
from urllib.parse import urljoin

def get_tms_cookie():
    """
    自动登录TMS系统并获取Cookie
    """
    # 登录URL
    login_url = 'https://tms.51talk.com/admin/admin_login.php'

    # 登录凭据
    credentials = {
        'username': 'admin',
        'password': '51talk20250227#'
    }

    # 创建session保持会话
    session = requests.Session()

    try:
        print(f"正在登录TMS系统: {login_url}")

        # 发送登录请求
        response = session.post(
            login_url,
            data=credentials,
            verify=False,  # 忽略SSL证书验证
            allow_redirects=True,
            timeout=30
        )

        print(f"登录响应状态码: {response.status_code}")
        print(f"响应内容(前500字符): {response.text[:500]}")

        # 获取Cookie
        cookies = session.cookies.get_dict()

        if cookies:
            # 将Cookie转换为字符串格式
            cookie_string = '; '.join([f"{key}={value}" for key, value in cookies.items()])

            print(f"\n成功获取Cookie:")
            print(f"Cookie内容: {cookie_string}")

            # 保存到配置文件
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'config',
                'tms_config.json'
            )

            config = {
                'cookie': cookie_string
            }

            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            print(f"\nCookie已保存到: {config_path}")
            return cookie_string
        else:
            print("\n警告: 未获取到Cookie,可能登录失败")
            print("请检查:")
            print("1. 用户名和密码是否正确")
            print("2. 登录URL是否正确")
            print("3. 是否需要验证码")
            return None

    except Exception as e:
        print(f"\n错误: 获取Cookie失败: {e}")
        return None

if __name__ == '__main__':
    # 禁用SSL警告
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    cookie = get_tms_cookie()

    if cookie:
        print("\n✓ Cookie获取成功!")
        print("\n下一步:")
        print("1. 重启后端服务")
        print("2. 测试TMS接口调用")
    else:
        print("\n✗ Cookie获取失败,请手动获取Cookie")
        print("\n手动获取步骤:")
        print("1. 浏览器访问 https://tms.51talk.com/admin/admin_login.php")
        print("2. 登录后按F12,复制Cookie")
        print("3. 粘贴到 config/tms_config.json")

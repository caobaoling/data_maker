# 文件: tools/get_tms_cookie_browser.py
# 作者: Claude Code
# 创建日期: 2026/03/06
# 描述: 使用浏览器自动化获取TMS Cookie

import json
import os
import sys
from playwright.sync_api import sync_playwright
import urllib3

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_tms_cookie_with_browser():
    """
    使用Playwright打开真实浏览器登录TMS系统并获取Cookie
    """
    print("=" * 60)
    print("TMS Cookie 自动获取工具 (浏览器模式)")
    print("=" * 60)

    with sync_playwright() as p:
        # 启动浏览器 (使用Chromium)
        print("\n[1/5] 启动浏览器...")
        browser = p.chromium.launch(
            headless=False,  # 显示浏览器窗口
            args=['--ignore-certificate-errors']  # 忽略SSL证书错误
        )

        # 创建浏览器上下文
        context = browser.new_context(
            ignore_https_errors=True,
            viewport={'width': 1280, 'height': 720}
        )

        # 创建新页面
        page = context.new_page()

        try:
            # 访问登录页面
            login_url = 'https://tms.51talk.com/admin/admin_login.php'
            print(f"\n[2/5] 访问登录页面: {login_url}")
            page.goto(login_url, wait_until='networkidle', timeout=30000)

            # 等待页面加载
            print("\n[3/5] 等待登录表单加载...")
            page.wait_for_selector('input[name="user_name"]', timeout=10000)

            # 填写用户名
            print("\n[4/5] 填写登录信息...")
            page.fill('input[name="user_name"]', 'admin')
            print("  [OK] 用户名: admin")

            # 填写密码
            page.fill('input[name="password"]', '51talk20250227#')
            print("  [OK] 密码: ********")

            # 点击登录按钮
            print("\n[5/5] 提交登录...")
            page.click('input[type="submit"]')

            # 等待登录完成 (等待页面跳转，增加超时时间)
            try:
                page.wait_for_load_state('networkidle', timeout=30000)
            except:
                # 即使超时也继续，因为可能已经登录成功
                print("  [INFO] 页面加载超时，但继续检查登录状态...")

            # 等待一下确保Cookie已设置
            page.wait_for_timeout(2000)

            # 获取当前URL
            current_url = page.url
            print(f"\n登录后URL: {current_url}")

            # 检查是否登录成功
            if 'admin_login.php' in current_url:
                print("\n[ERROR] 登录失败: 仍在登录页面")
                print("可能原因:")
                print("  1. 用户名或密码错误")
                print("  2. 需要验证码")
                print("  3. 账号被锁定")

                # 截图保存
                screenshot_path = os.path.join(
                    os.path.dirname(__file__),
                    'tms_login_failed.png'
                )
                page.screenshot(path=screenshot_path)
                print(f"\n已保存截图: {screenshot_path}")

                browser.close()
                return None

            # 获取所有Cookie
            cookies = context.cookies()
            print(f"\n[SUCCESS] 登录成功! 获取到 {len(cookies)} 个Cookie")

            # 查找PHPSESSID
            phpsessid = None
            cookie_dict = {}

            for cookie in cookies:
                cookie_dict[cookie['name']] = cookie['value']
                if cookie['name'] == 'PHPSESSID':
                    phpsessid = cookie['value']
                    print(f"\n[SUCCESS] 找到PHPSESSID: {phpsessid}")

            if not phpsessid:
                print("\n[WARNING] 警告: 未找到PHPSESSID")
                print(f"可用的Cookie: {list(cookie_dict.keys())}")

            # 将Cookie转换为字符串格式
            cookie_string = '; '.join([f"{k}={v}" for k, v in cookie_dict.items()])

            # 保存到配置文件
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'config',
                'tms_config.json'
            )

            config = {
                'cookie': cookie_string,
                'phpsessid': phpsessid,
                'obtained_at': page.evaluate('new Date().toISOString()')
            }

            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            print(f"\n[SUCCESS] Cookie已保存到: {config_path}")
            print("\nCookie内容:")
            print(f"  {cookie_string[:100]}...")

            # 保持浏览器打开3秒让用户看到结果
            print("\n浏览器将在3秒后关闭...")
            page.wait_for_timeout(3000)

            browser.close()
            return cookie_string

        except Exception as e:
            print(f"\n[ERROR] 错误: {e}")

            # 截图保存
            try:
                screenshot_path = os.path.join(
                    os.path.dirname(__file__),
                    'tms_error.png'
                )
                page.screenshot(path=screenshot_path)
                print(f"\n已保存错误截图: {screenshot_path}")
            except:
                pass

            browser.close()
            return None

if __name__ == '__main__':
    print("\n提示: 请确保已安装Playwright浏览器驱动")
    print("如果未安装,请运行: python -m playwright install chromium\n")

    cookie = get_tms_cookie_with_browser()

    if cookie:
        print("\n" + "=" * 60)
        print("[SUCCESS] Cookie获取成功!")
        print("=" * 60)
        print("\n下一步:")
        print("1. 重启后端服务")
        print("2. 测试TMS接口调用")
    else:
        print("\n" + "=" * 60)
        print("[FAILED] Cookie获取失败")
        print("=" * 60)
        print("\n请检查:")
        print("1. 网络连接是否正常")
        print("2. TMS系统是否可访问")
        print("3. 用户名密码是否正确")

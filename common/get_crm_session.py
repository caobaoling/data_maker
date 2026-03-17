# 文件: common/get_crm_session.py
# 作者: Claude Code
# 创建日期: 2026/03/06
# 描述: CRM系统客户端，提供登录和接口调用功能

import logging
import requests
import urllib3
import hashlib
from .env_utils import get_request_with_host_override

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)


class CRMClient:
    """CRM系统客户端"""

    def __init__(self, username='admin', password='51talk20250227#'):
        """
        初始化CRM客户端

        Args:
            username: CRM用户名
            password: CRM密码
        """
        self.username = username
        self.password = password
        self.session = None
        self.base_url = 'https://crm.51talk.com'

    def login(self):
        """
        登录CRM系统

        Returns:
            bool: 登录是否成功
        """
        try:
            self.session = requests.Session()
            login_url = f'{self.base_url}/admin/login.php'
            password_md5 = hashlib.md5(self.password.encode()).hexdigest()

            credentials = {
                'user_name': self.username,
                'password': password_md5,
                'ref': '',
                'user_type': 'admin',
                'login_type': 'tmp'
            }

            logger.info(f"[CRM登录] 正在登录CRM系统...")

            response = self.session.post(
                login_url,
                data=credentials,
                verify=False,
                allow_redirects=True,
                timeout=30
            )

            if response.status_code == 200:
                cookies = self.session.cookies.get_dict()
                admin_code = cookies.get('admin_code')

                if admin_code:
                    logger.info(f"[CRM登录] 登录成功")
                    return True
                else:
                    # 添加详细的调试信息
                    logger.error(f"[CRM登录] 登录失败,未获取到admin_code")
                    logger.error(f"[CRM登录] 响应状态码: {response.status_code}")
                    logger.error(f"[CRM登录] 响应Cookies: {cookies}")
                    logger.error(f"[CRM登录] 响应内容前500字符: {response.text[:500]}")
                    return False
            else:
                logger.error(f"[CRM登录] 登录失败,状态码: {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"[CRM登录] 登录异常: {e}")
            return False

    def get_session(self):
        """
        获取已登录的Session对象

        Returns:
            requests.Session: 已登录的Session对象，如果未登录则返回None
        """
        if self.session is None:
            if not self.login():
                return None
        return self.session

    def call_api(self, endpoint, method='GET', params=None, data=None, timeout=30):
        """
        调用CRM接口 (自动适配测试/生产环境)

        Args:
            endpoint: 接口路径（如 '/tea_promotion/batchUpdateTeacherInfo'）
            method: HTTP方法（GET/POST）
            params: URL参数
            data: POST数据
            timeout: 超时时间（秒）

        Returns:
            requests.Response: 响应对象，失败返回None
        """
        session = self.get_session()
        if not session:
            logger.error("[CRM接口] 未登录，无法调用接口")
            return None

        try:
            url = f'{self.base_url}{endpoint}'

            # 使用环境适配方法发送请求
            response = get_request_with_host_override(
                session,
                url,
                method=method,
                params=params,
                data=data,
                timeout=timeout,
                verify=False
            )

            return response

        except Exception as e:
            logger.error(f"[CRM接口] 调用失败: {e}")
            return None

    def close(self):
        """关闭Session"""
        if self.session:
            self.session.close()
            self.session = None


def get_crm_session(username='admin', password='51talk20250227#'):
    """
    获取CRM Session的便捷函数

    Args:
        username: CRM用户名
        password: CRM密码

    Returns:
        requests.Session: 已登录的Session对象，失败返回None
    """
    client = CRMClient(username, password)
    return client.get_session()

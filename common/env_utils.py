# 文件: common/env_utils.py
# 作者: Claude Code
# 创建日期: 2026/03/06
# 描述: 环境判断和请求Host修改工具

import os
import socket
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.connection import create_connection

logger = logging.getLogger(__name__)

# 测试环境的Host映射配置
TEST_ENV_HOSTS = {
    'tms.51talk.com': '172.16.0.54'
}


def is_test_environment():
    """
    判断当前是否为测试环境

    判断逻辑:
    1. 检查环境变量 ENVIRONMENT 是否为 'test'
    2. 检查是否能解析到测试环境的IP (172.16.0.54)

    Returns:
        bool: True表示测试环境, False表示生产环境
    """
    # 方式1: 通过环境变量判断
    env = os.environ.get('ENVIRONMENT', '').lower()
    if env == 'test':
        logger.info("[环境判断] 通过环境变量判断为测试环境")
        return True

    # 方式2: 通过DNS解析判断 (检查tms.51talk.com是否解析到测试IP)
    try:
        resolved_ip = socket.gethostbyname('tms.51talk.com')
        if resolved_ip == '172.16.0.54':
            logger.info(f"[环境判断] 通过DNS解析判断为测试环境 (IP: {resolved_ip})")
            return True
        else:
            logger.info(f"[环境判断] 判断为生产环境 (DNS解析IP: {resolved_ip})")
            return False
    except Exception as e:
        logger.warning(f"[环境判断] DNS解析失败: {e}, 默认判断为生产环境")
        return False


class HostHeaderAdapter(HTTPAdapter):
    """
    自定义HTTP适配器，用于在测试环境中修改DNS解析
    保持URL中的域名不变，但实际连接到指定的IP地址
    """

    def __init__(self, host_mapping=None, *args, **kwargs):
        """
        初始化适配器

        Args:
            host_mapping: 域名到IP的映射字典，如 {'tms.51talk.com': '172.16.0.54'}
        """
        self.host_mapping = host_mapping or {}
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        """初始化连接池管理器，注入自定义的DNS解析函数"""
        # 保存原始的 create_connection 函数
        original_create_connection = create_connection

        # 创建自定义的连接函数
        def patched_create_connection(address, *args, **kwargs):
            host, port = address
            # 如果域名在映射表中，替换为指定的IP
            if host in self.host_mapping:
                logger.info(f"[DNS重定向] {host} -> {self.host_mapping[host]}")
                address = (self.host_mapping[host], port)
            return original_create_connection(address, *args, **kwargs)

        # 临时替换 create_connection 函数
        import urllib3.util.connection
        urllib3.util.connection.create_connection = patched_create_connection

        try:
            super().init_poolmanager(*args, **kwargs)
        finally:
            # 恢复原始函数
            urllib3.util.connection.create_connection = original_create_connection


def setup_session_for_environment(session):
    """
    根据环境配置Session的适配器

    Args:
        session: requests.Session对象

    Returns:
        requests.Session: 配置好的Session对象
    """
    if is_test_environment():
        # 测试环境：使用自定义适配器进行DNS重定向
        adapter = HostHeaderAdapter(host_mapping=TEST_ENV_HOSTS)
        session.mount('https://', adapter)
        session.mount('http://', adapter)
        logger.info("[环境配置] 已配置测试环境DNS重定向")
    else:
        logger.info("[环境配置] 生产环境，使用默认配置")

    return session


def get_request_with_host_override(session, url, method='GET', **kwargs):
    """
    发送HTTP请求，根据环境自动处理Host头

    在测试环境中，保持URL中的域名不变，但通过自定义适配器将实际连接重定向到测试IP

    Args:
        session: requests.Session对象
        url: 请求URL (如 'https://tms.51talk.com/tea_promotion/...')
        method: HTTP方法 ('GET' 或 'POST')
        **kwargs: 其他requests参数 (params, data, timeout等)

    Returns:
        requests.Response: 响应对象

    示例:
        session = requests.Session()
        response = get_request_with_host_override(
            session,
            'https://tms.51talk.com/tea_promotion/batchUpdateTeacherInfo',
            method='GET',
            params={'t_ids': '12345'},
            timeout=30,
            verify=False
        )
    """
    # 确保Session已配置环境适配器
    setup_session_for_environment(session)

    # 直接使用原始URL发送请求，适配器会自动处理DNS重定向
    if method.upper() == 'GET':
        return session.get(url, **kwargs)
    elif method.upper() == 'POST':
        return session.post(url, **kwargs)
    else:
        raise ValueError(f"不支持的HTTP方法: {method}")

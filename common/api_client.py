# 文件: api_client
# 作者: bao0
# 创建日期: 2024/12/5
# 描述: 这是一个发送 HTTP 请求的通用方法

import requests


def send_request_get(url, params):
    """发送 HTTP GET 请求并返回响应"""
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # 如果响应状态码不是 200，会抛出 HTTPError 异常
        return response.json()  # 假设响应内容是 JSON 格式
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None


def send_request_post(url, params):
    """发送 HTTP POST 请求并返回响应"""
    try:
        # 修复：使用 json= 而不是 params= 来发送POST body
        response = requests.post(url, json=params)
        response.raise_for_status()  # 如果响应状态码不是 200，会抛出 HTTPError 异常
        return response.json()  # 假设响应内容是 JSON 格式
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return {"code": "50000", "message": f"请求失败: {e}", "data": None}

# 文件: elf_create_endclass
# 作者: bao0
# 创建日期: 2024/10/23
# 描述: 这是一个给用户创建新任务的方法-精灵
import requests
import time

from common.api_client import send_request_post

# 定义 API URL
# 测试环境
url = 'http://172.16.16.36:10006/talkplatform_game/v1/rank/user_settle'

stu_id = 66
biz_id = 578473706   # 约课id

# 获取当前时间戳（秒）
timestamp_seconds = int(time.time())
# print(timestamp_seconds)

# 定义查询参数
params = {
    'stu_id': stu_id,
    'type': '2',
    'appkey': 'java',
    'timestamp': timestamp_seconds,
    'biz_id': biz_id
}

# 发送请求
response_data = send_request_post(url, params)
# print(response_data)
# 校验返回值
if 'code' in response_data and response_data['code'] == '10000':
    print("请求成功，返回数据:", response_data)
else:
    print(f"请求失败，返回码: {response_data.get('code', '未知')}, 错误信息: {response_data.get('message', '未知')}")


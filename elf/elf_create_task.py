# 文件: elf_create_task
# 作者: bao0
# 创建日期: 2024/10/23
# 描述: 这是一个给用户创建新任务的方法-精灵
import requests
import time

from common.api_client import send_request_get

# 定义 API URL
# 测试环境
url = 'http://172.16.16.36/talkplatform_task_consumer/task/user_task/v1/front/query_in_cycle_user_task_list'
# 线上环境
# url = 'http://192.168.24.106/talkplatform_task_consumer/task/user_task/v1/front/query_in_cycle_user_task_list'
stu_id = 1587393646


# 获取当前时间戳（秒）
timestamp_seconds = int(time.time())
# print(timestamp_seconds)

# 定义查询参数
params = {
    'biz_category': 'game_system',
    'user_id': stu_id,
    'appkey': 'java',
    'timestamp': timestamp_seconds,
    'task_biz_category_list': 'elf_week_task,elf_month_task'
}

# 发送请求
response_data = send_request_get(url, params)
# print(response_data)
# 校验返回值
if 'code' in response_data and response_data['code'] == '10000':
    print("请求成功，返回数据:", response_data)
else:
    print(f"请求失败，返回码: {response_data.get('code', '未知')}, 错误信息: {response_data.get('message', '未知')}")


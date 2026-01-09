# 文件: high_risk_user_device
# 作者: bao0
# 创建日期: 2025/4/2
# 描述: 这是一个解决用户登录多台设备限制登录的方法
# 1、用户解除高风险2、添加白名单的方法
import time

from common.api_client import send_request_get, send_request_post

# 定义 API URL
# 线上环境
base_url = 'http://10.0.112.226'  # 境内
# base_url = 'http://192.168.27.35'  # 境外
release_url = f'{base_url}/api/high_risk_user_device/release'
whitelist_url = f'{base_url}/api/high_risk_user_device/add_white_list'

stu_id = 58024245

# 获取当前时间戳（秒）
timestamp_seconds = int(time.time())
# print(timestamp_seconds)

# 定义变量
risk_item = '58024245'  # risk_item 设备或用户id
risk_type = '2'  # risk_type 1 设备 2 用户
operator_id = '124'
appkey = 'erp'

# 定义解除高风险的查询参数
release_params = {
    'stu_id': stu_id,
    'risk_type': risk_type,
    'appkey': appkey,
    'timestamp': timestamp_seconds,
    'risk_item': risk_item,
    'status': '2'
}

# 发送解除高风险请求
response_data_release = send_request_post(release_url, release_params)
print(response_data_release)
# 校验返回值
if 'code' in response_data_release and response_data_release['code'] == 10000:
    print("解除高风险请求成功，返回数据:", response_data_release)
else:
    print(
        f"解除高风险请求失败，返回码: {response_data_release.get('code', '未知')}, 错误信息: {response_data_release.get('message', '未知')}")

# 定义添加白名单的查询参数
whitelist_params = {
    'appkey': appkey,
    'timestamp': timestamp_seconds,
    'risk_type': risk_type,
    'risk_item': risk_item,
    'operator_id': operator_id
}

# 发送添加白名单请求
response_data_whitelist = send_request_get(whitelist_url, whitelist_params)
# print(response_data_whitelist)
# 校验返回值
if 'code' in response_data_whitelist and response_data_whitelist['code'] == 10000:
    print("添加白名单请求成功，返回数据:", response_data_whitelist)
else:
    print(
        f"添加白名单请求失败，返回码: {response_data_whitelist.get('code', '未知')}, 错误信息: {response_data_whitelist.get('message', '未知')}")

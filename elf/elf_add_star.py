# 文件: elf_add_star
# 作者: bao0
# 创建日期: 2024/10/31
# 描述: 这是一个给课程添加星星方法
import requests
import time

from common.api_client import send_request_get

# 定义 API URL
url = 'https://appi.51talkglobal.com/User/sendStar'
# url = 'https://172.16.70.59/User/sendStar'
stu_id = 1587401021
appoint_id = 916929660

# 获取当前时间戳（秒）
timestamp_seconds = int(time.time())
# print(timestamp_seconds)

# 定义查询参数
params = {
    'biz_category': 'game_system',
    'tsign':'F72C2788F98F1555779C59FC4AF34D94',
    'talk_token':'bl%7CjnoQqt-nkHuy0pvsReULc0WZDgxh9SNxVuf7nCAQTtJ3IeGNvBsX1NDzU4x7TZCaDbaob7AdwCGbsUc6Fs5EZDX9%2FUM2CXmRf0RnP3A%3D',
    'userId': stu_id,
    'stu_id': stu_id,
    'star_num': 2,
    'resolution': '2560_1600',
    'physics_size': '10.8',
    'device_mod': 'MRX-AL09&oaid=efd76ff9-f9e5-90e4-8dd7-dc9f7f5f209c',
    'device_firm': 'HUAWEI',
    'client_id': '86794e128dccc9646eb48883e7880655',
    'appoint_id': appoint_id,
    'appkey': 'junior_app',
    'phoneType': 'andrKid',
    'deviceType': 'HUAWEI_MRX-AL09',
    'deviceId': '6281638E49D54D7384A70EEA736E1F88',
    'systemVer': '31',
    'channel': 'hicloud',
    'version': '6.1.7',
    'appkey': 'java',
    'timestamp': timestamp_seconds,
    'task_biz_category_list': 'elf_week_task,elf_month_task'
}

# 发送请求
response_data = send_request_get(url, params)
print(response_data)
# 校验返回值
if 'code' in response_data and response_data['code'] == '10000':
    print("请求成功，返回数据:", response_data)
else:
    print(f"请求失败，返回码: {response_data.get('code', '未知')}, 错误信息: {response_data.get('res', '未知')}")




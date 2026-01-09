# 文件: change_appoint_status
# 作者: bao0
# 创建日期: 2024/10/23
# 描述: 这是一个更改约课状态的方法
import time

import requests
import json

# 定义 API URL
url = 'http://172.16.16.97/talkplatform_appointone_consumer/v1/appoint/update'
appoint_id = "620668693"
# status = "cancel"
# status = "s_absent"
# status = "t_absent"
# status = "on"
status = "end"
stamp_time = int(time.time())
# 定义请求体数据
data = {
    "id": appoint_id,
    "status": status,
    "cancel_time": stamp_time,
    "update_time": stamp_time,
}

# 将数据转换为 JSON 格式
json_data = json.dumps(data)

# 发送 POST 请求
response = requests.post(url, data=json_data, headers={'Content-Type': 'application/json'})

# 检查请求是否成功
if response.status_code == 200:
    # 解析响应内容
    data = response.json()  # 假设响应内容是 JSON 格式
    print(data)
else:
    print(f"请求失败，状态码: {response.status_code}")
    print(f"响应内容: {response.text}")

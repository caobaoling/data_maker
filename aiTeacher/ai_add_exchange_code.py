# 文件: ai_add_exchange_code.
# 作者: bao0
# 创建日期: 2025/5/28
# 描述: 这是一个给AI外教账号添加兑换码的方法

import requests

order_exchange_code = "37e6d355095ce3973e11f65d3949b8fa"
user_id= "1587402855"

# 定义 API URL
url = 'http://172.16.16.36/talkplatform_leads_consumer/leads/third/tiktok/v1/front/user_exchange_order?order_exchange_code='+ order_exchange_code +'&user_id='+ user_id

# 发送 POST 请求
response = requests.post(url,  headers={'Content-Type': 'application/json'})

# 检查请求是否成功
if response.status_code == 200:
    # 解析响应内容
    data = response.json()  # 假设响应内容是 JSON 格式
    print(data)
else:
    print(f"请求失败，状态码: {response.status_code}")
    print(f"响应内容: {response.text}")

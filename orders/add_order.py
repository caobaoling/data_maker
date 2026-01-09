# 文件: add_appoint
# 作者: bao0
# 创建日期: 2025/04/29
# 描述: 这是一个给用户添加订单的方法
import current_time
import requests
import time
import random

from datetime import datetime, timedelta
# 定义 API URL
url = 'http://172.16.16.97/talkplatform_order_consumer/v1/order/add'





# 定义查询参数
data = {
"order_money": 1599,
"deal_time": "2025-4-29",
"cash_card": 649379,
"remark": "kfdjfd98",
"content": [{"goods_id": 263147, "type": "product"}],
"operator": 343,
"from_url_id": 4793874,
"bank": "zh",
"user_type": 1,
"business_type": "51talk",
"recommend_id": 6878,
"order_type": "point_package",
"timestamp": "current_time.strftime('%Y-%m-%d %H:%M:%S')",
"phone_package": 200,
"from_type": "web",
"discount_money": 100,
"refund_status": 0,
"sales_content": [{"type": "3", "num": "2", "money": "100"}, {"type": "1", "num": "1", "money": "200"}],
"is_new": 0,
"custom_id": 4422,
"pay_method": "Bank",
"discount_type": "cash_down",
"month_start_date": "2019-03-25",
"buy_costomer": 7398,
"app_key": "front",
"order_num": 89,
"gateway": "bank",
"status": "on",
"remark2": "089ioj",
"appkey": 60506,
"display_money": 5299,
"id": 743866885,
"stu_id": 1587401666,
"extend_id": 263147
}
# 定义自定义头部
headers = {
    'Authorization': 'Bearer your_token',
    'Content-Type': 'application/json'
}
# 发送 POST 请求
response = requests.post(url, json=data, headers=headers)
# 检查请求是否成功
if response.status_code == 200:
    # 解析响应内容
    data = response.json()  # 假设响应内容是 JSON 格式
    print(data)
else:
    print(f"请求失败，状态码: {response.status_code}")
    print(f"响应内容: {response.text}")


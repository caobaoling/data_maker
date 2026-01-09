# 文件: add_appoint
# 作者: bao0
# 创建日期: 2025/06/218
# 描述: 这是一个给用户添加财富的方法
import requests
import time

# 定义 API URL
url = 'http://172.16.16.36/talkplatform_point_consumer/v2/user_asset/backend/add_gift_asset'

stu_id = '1587398158'
# 获取当前时间戳（秒）
timestamp = int(time.time())

# 定义查询参数
form = "sn=ai_teacher&stu_id={}&count=100&sku_type_name=ai_teach&transaction_type_code=add_gift_asset&operator_id=0&days=365&remark=ai外教内测赠送&timestamp={}&appkey=java".format(stu_id, timestamp)
print(form)
# 定义自定义头部
headers = {
    # 'Authorization': 'Bearer your_token',
    'Content-Type': 'application/json'
}
# 发送 POST 请求
response = requests.post(url = url, data = form)
# 检查请求是否成功
if response.status_code == 200:
    # 解析响应内容
    data = response.json()  # 假设响应内容是 JSON 格式
    print(data)
else:
    print(f"请求失败，状态码: {response.status_code}")
    print(f"响应内容: {response.text}")


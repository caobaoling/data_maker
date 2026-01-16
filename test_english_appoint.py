"""
测试英语预约API
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5001/api"

# 测试数据（使用推荐的教师ID）
data = {
    "stu_id": "1587393646",
    "t_id": "2821",  # 推荐的英语教师ID
    "start_time": "2026-01-16 10:00:00",
    "end_time": "2026-01-16 10:30:00",
    "date_time": "20260116_21",
    "course_type": "1",
    "point_type": "point",
    "use_point": "buy",
    "status": "on",
    "course_id": "793041",
    "course_top_id": "773011",
    "course_sub_id": "793011",
    "remark": ""
}

print("=" * 60)
print("测试英语预约API")
print("=" * 60)
print(f"\n发送数据:\n{json.dumps(data, ensure_ascii=False, indent=2)}")

try:
    response = requests.post(
        f"{BASE_URL}/appoint/add_en",
        json=data,
        headers={"Content-Type": "application/json"}
    )

    print(f"\n响应状态码: {response.status_code}")
    print(f"响应数据:\n{json.dumps(response.json(), ensure_ascii=False, indent=2)}")

    result = response.json()
    if result.get("code") == "10000":
        print("\n[SUCCESS] 英语预约创建成功!")
        print(f"预约ID: {result.get('res', {}).get('id')}")
    else:
        print(f"\n[ERROR] 创建失败: {result.get('message')}")

except Exception as e:
    print(f"\n[ERROR] 请求异常: {str(e)}")

print("\n" + "=" * 60)

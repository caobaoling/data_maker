"""
API测试脚本 - 测试添加预约和状态变更功能
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5001/api"

def test_health():
    """测试健康检查"""
    try:
        response = requests.get(f"{BASE_URL.replace('/api', '')}/api/health")
        print(f"[OK] 健康检查: {response.json()}")
        return True
    except Exception as e:
        print(f"[ERROR] 健康检查失败: {e}")
        return False

def test_add_appoint_cn():
    """测试添加普通话预约"""
    now = datetime.now()
    # 确保是整点或半点
    if now.minute < 30:
        start_time = now.replace(minute=0, second=0, microsecond=0)
    else:
        start_time = now.replace(minute=30, second=0, microsecond=0)

    end_time = start_time + timedelta(minutes=30)

    data = {
        "stu_id": "12345678",
        "t_id": "350012781",
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
        "date_time": start_time.strftime("%Y%m%d") + f"_{start_time.hour * 2 + (2 if start_time.minute >= 30 else 1)}",
        "course_type": "31",
        "point_type": "pthpoint",
        "use_point": "buy",
        "status": "on",
        "course_id": "1406031",
        "course_top_id": "1400011",
        "course_sub_id": "1406021"
    }

    print("\n测试添加普通话预约:")
    print(f"请求数据: {json.dumps(data, ensure_ascii=False, indent=2)}")

    try:
        response = requests.post(
            f"{BASE_URL}/appoint/add_cn",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"响应状态码: {response.status_code}")
        print(f"响应数据: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        return response.json()
    except Exception as e:
        print(f"[ERROR] 添加预约失败: {e}")
        return None

def test_update_status(appoint_id):
    """测试更新预约状态"""
    data = {
        "id": appoint_id,
        "status": "end"
    }

    print("\n测试修改预约状态:")
    print(f"请求数据: {json.dumps(data, ensure_ascii=False, indent=2)}")

    try:
        response = requests.post(
            f"{BASE_URL}/appoint/update_status",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"响应状态码: {response.status_code}")
        print(f"响应数据: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        return response.json()
    except Exception as e:
        print(f"[ERROR] 状态变更失败: {e}")
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("DataMaker API 测试")
    print("=" * 60)

    # 1. 测试健康检查
    if not test_health():
        print("\n[WARNING] 后端服务未启动，请先启动后端:")
        print("cd backend && python app.py")
        exit(1)

    # 2. 测试添加预约
    result = test_add_appoint_cn()

    if result and result.get("code") == "10000":
        print("\n[SUCCESS] 添加预约成功!")
        appoint_id = result.get("res", {}).get("id")

        if appoint_id:
            # 3. 测试状态变更
            test_update_status(appoint_id)
    else:
        print("\n[ERROR] 添加预约失败，请查看上面的错误信息")

    print("\n" + "=" * 60)

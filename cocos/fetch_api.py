import requests
import json
import os
import sys
import time
import pymysql

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from common.db_utils import load_config

COURSE_TYPES = {
    "100": "阅读",
    "101": "词汇",
    "102": "字母",
    "103": "自拼",
    "104": "嘉年华",
    "105": "对话",
}

def fetch(appoint_id: str, course_id: str, suffix: str):
    # 从数据库查询 id
    cfg = load_config()
    conn = pymysql.connect(
        host=cfg['host'], port=cfg['port'],
        user=cfg['user'], password=cfg['password'],
        db='midplatform_user_learning', charset='utf8mb4'
    )
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM midplatform_user_learning.user_material_progress WHERE appoint_id = %s",
        (appoint_id,)
    )
    row = cur.fetchone()
    conn.close()

    if not row:
        print(f"[fetch_api] 未查到 appoint_id={appoint_id} 对应的 id")
        return False

    material_id = str(row[0])
    course_name = COURSE_TYPES.get(appoint_id, '')
    print(f"[fetch_api] appoint_id={appoint_id}({course_name}) → id={material_id}")

    #测试环境
    url = "http://172.16.70.131:10014/midplatform_user_learning_schedule/api/datasource/post_class_remmment"
    #线上环境-境内
    #url = "http://10.0.18.156:8080/midplatform_user_learning_schedule/api/datasource/post_class_remmment"
    #线上环境-境外
    #url = "http://192.168.65.156:8080/midplatform_user_learning_schedule/api/datasource/post_class_remmment"
    params = {
        "id": material_id,
        "appkey": "java",
        "timestamp": str(int(time.time() * 1000)),
        "language": "ja",
        "user_name": "Tom"
    }

    response = requests.get(url, params=params, timeout=30)
    print(f"完整请求URL：{response.url}")

    result = response.json()

    # 保持原来的 json.json
    out_path = os.path.join(os.path.dirname(__file__), "json.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    save_dir = os.path.join(
        os.path.dirname(__file__),
        "6种课型的接口返回json"
    )
    os.makedirs(save_dir, exist_ok=True)

    course_name = COURSE_TYPES[course_id]

    filename = f"{course_id}{course_name}{suffix}.json"

    lesson_path = os.path.join(save_dir, filename)

    with open(lesson_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"已保存：{lesson_path}")
    return True

def run(appoint_ids, suffix):
    for appoint_id in appoint_ids:
        print(f"\n========== {appoint_id}{COURSE_TYPES[appoint_id]} ==========")
        fetch(appoint_id, appoint_id, suffix)

if __name__ == "__main__":
    
    suffix = sys.argv[1] if len(sys.argv) > 1 else None

    if not suffix:
        print("用法：python fetch_api.py moderate_mastery")
        sys.exit(1)

    for course_id in COURSE_TYPES:
        print(f"\n========== 开始获取 {course_id}{COURSE_TYPES[course_id]} ==========")

        fetch(appoint_id, course_id, suffix)
        
    run(list(COURSE_TYPES.keys()), suffix)

import requests
import json
import os
import sys
import time
import pymysql

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from common.db_utils import load_config


def fetch(appoint_id: str):
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
    print(f"[fetch_api] appoint_id={appoint_id} → id={material_id}")

    #测试环境
    #url = "http://172.16.70.131:10014/midplatform_user_learning_schedule/api/datasource/post_class_remmment"
    #线上环境
    url = "http://10.0.18.156:8080/midplatform_user_learning_schedule/api/datasource/post_class_remmment"
    params = {
        "id": material_id,
        "appkey": "java",
        "timestamp": str(int(time.time() * 1000))
    }

    response = requests.get(url, params=params, timeout=30)
    print(f"完整请求URL：{response.url}")

    result = response.json()
    out_path = os.path.join(os.path.dirname(__file__), "json.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"状态码: {response.status_code}")
    print(f"结果已保存到 {out_path}")
    return True


if __name__ == '__main__':
    appoint_id = sys.argv[1] if len(sys.argv) > 1 else None
    if not appoint_id:
        print("用法: python cocos/fetch_api.py <appoint_id>")
        sys.exit(1)
    fetch(appoint_id)

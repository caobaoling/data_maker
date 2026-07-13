# -*- coding: utf-8 -*-
"""
reset_mastery.py
作者: bao0
描述: 查询指定 appoint_id 下的 knowledge_id，批量调用接口将 mastery 重置为指定值

用法:
  python cocos/reset_mastery.py [mastery]
  python cocos/reset_mastery.py not_mastered

mastery 可选值: not_mastered / moderate_mastery / excellent_mastery / perfect_mastery
默认值: not_mastered
"""

import sys
import os
import time
import requests
import pymysql

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from common.db_utils import load_config

# ─────────────────────────────────────────────────────────
# 配置
# ─────────────────────────────────────────────────────────
APPOINT_IDS = ['100', '101', '102', '103', '104', '105']
#APPOINT_IDS = ['100']

VALID_MASTERY_VALUES = {
    'not_mastered',
    'moderate_mastery',
    'excellent_mastery',
    'perfect_mastery',
}

API_URL = 'http://10.0.18.89:8080/midplatform_user_learning/user_appoint_knowledge_mastery/update_mastery'


# ─────────────────────────────────────────────────────────
# 1. 从数据库查询 knowledge_id 列表
# ─────────────────────────────────────────────────────────
def load_knowledge_ids(appoint_ids: list) -> list:
    cfg = load_config()
    conn = pymysql.connect(
        host=cfg['host'],
        port=cfg['port'],
        user=cfg['user'],
        password=cfg['password'],
        database='midplatform_user_learning',
        charset='utf8mb4',
    )
    placeholders = ', '.join(['%s'] * len(appoint_ids))
    sql = f"""
        SELECT knowledge_id
        FROM `midplatform_user_learning`.`user_appoint_knowledge_mastery`
        WHERE `appoint_id` IN ({placeholders})
        ORDER BY `create_time`
        LIMIT 0, 1000
    """
    with conn:
        with conn.cursor() as cur:
            cur.execute(sql, appoint_ids)
            rows = cur.fetchall()

    return [str(row[0]) for row in rows]


# ─────────────────────────────────────────────────────────
# 2. 调用接口批量更新 mastery
# ─────────────────────────────────────────────────────────
def update_mastery(knowledge_ids: list, mastery: str):
    total   = len(knowledge_ids)
    success = 0
    failed  = []

    for i, kid in enumerate(knowledge_ids, 1):
        params = {
            'id':        kid,
            'mastery':   mastery,
            'appkey':    'java',
            'timestamp': str(int(time.time() * 1000)),
        }
        try:
            resp = requests.post(
                API_URL,
                params=params,
                headers={'User-Agent': 'Apipost/8 (https://www.apipost.cn)'},
                timeout=10,
            )
            result = resp.json() if resp.headers.get('content-type', '').startswith('application/json') else resp.text
            ok = resp.status_code == 200
            print(f"  [{i}/{total}] id={kid} | status={resp.status_code} | resp={result}")
            if ok:
                success += 1
            else:
                failed.append(kid)
        except Exception as e:
            print(f"  [{i}/{total}] id={kid} | 请求异常: {e}")
            failed.append(kid)

    print()
    print(f"  汇总: 成功={success}  失败={len(failed)}  共={total}")
    if failed:
        print(f"  失败的 knowledge_id: {failed}")


# ─────────────────────────────────────────────────────────
# 入口
# ─────────────────────────────────────────────────────────
if __name__ == '__main__':
    mastery = sys.argv[1] if len(sys.argv) > 1 else 'not_mastered'

    if mastery not in VALID_MASTERY_VALUES:
        print(f"[错误] 不合法的 mastery 值: {mastery}")
        print(f"  可选值: {', '.join(sorted(VALID_MASTERY_VALUES))}")
        sys.exit(1)

    print(f"appoint_ids: {APPOINT_IDS}")
    print(f"目标 mastery: {mastery}")

    print(f"\n[1] 查询数据库 knowledge_id ...")
    kids = load_knowledge_ids(APPOINT_IDS)
    print(f"    共 {len(kids)} 条")
    for kid in kids:
        print(f"    knowledge_id={kid}")

    if not kids:
        print("[跳过] 未查到知识点，退出")
        sys.exit(0)

    print(f"\n[2] 批量调用接口更新 mastery={mastery} ...")
    update_mastery(kids, mastery)

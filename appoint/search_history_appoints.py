# 文件: search_history_appoints.py
# 作者: bao0
# 创建日期: 2024/12/18
# 描述: 查询用户约课历史数据

import sys
import os
import time
import json
from datetime import datetime, timedelta

# 添加项目根目录以导入common模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.api_client import send_request_get
from common.db_connect import create_connection


def search_user_appointments_from_db(stu_id, limit=1000, offset=0, course_type=None, status=None):
    """
    从数据库查询用户所有约课数据

    参数:
        stu_id: 学生ID (必需)
        limit: 返回记录数限制 (默认1000)
        offset: 偏移量，用于分页 (默认0)
        course_type: 课程类型过滤，可选 (1=英语, 31=普通话)
        status: 状态过滤，可选 (on=正常, cancel=取消)

    返回:
        查询结果字典 {total, count, data}
    """
    print(f"\n{'='*60}")
    print(f"从数据库查询用户约课数据")
    print(f"{'='*60}")
    print(f"学生ID: {stu_id}")
    print(f"查询限制: {limit} 条，偏移: {offset}")
    if course_type:
        print(f"课程类型过滤: {'英语' if course_type == '1' else '普通话' if course_type == '31' else course_type}")
    if status:
        print(f"状态过滤: {status}")
    print(f"{'='*60}\n")

    # 连接数据库
    conn = create_connection()
    if not conn:
        print("[ERROR] 数据库连接失败")
        return None

    try:
        cursor = conn.cursor()

        # 构建WHERE条件
        conditions = [f"s_id = '{stu_id}'"]
        if course_type:
            conditions.append(f"course_type = '{course_type}'")
        if status:
            conditions.append(f"status = '{status}'")

        where_clause = " AND ".join(conditions)

        # 先查询总数
        count_sql = f"SELECT COUNT(*) as total FROM `talkplatform_appoint_reconstruction`.`appoint` WHERE {where_clause}"
        cursor.execute(count_sql)
        total = cursor.fetchone()[0]
        print(f"[INFO] 数据库中共找到 {total} 条记录\n")

        # 查询数据
        query_sql = f"""
            SELECT
                id, s_id, t_id, start_time, end_time, status,
                course_type, point_type, use_point, category,
                course_id, course_top_id, course_sub_id,
                add_time, date_time, date, time
            FROM `talkplatform_appoint_reconstruction`.`appoint`
            WHERE {where_clause}
            ORDER BY id DESC
            LIMIT {limit} OFFSET {offset}
        """

        print(f"[SQL] {query_sql[:200]}...\n")
        cursor.execute(query_sql)

        # 获取列名
        columns = [desc[0] for desc in cursor.description]

        # 转换为字典列表
        rows = cursor.fetchall()
        result_list = []
        for row in rows:
            item = dict(zip(columns, row))
            # 转换datetime对象为字符串
            for key in ['start_time', 'end_time', 'add_time']:
                if key in item and item[key]:
                    item[key] = str(item[key])
            result_list.append(item)

        cursor.close()
        conn.close()

        print(f"[SUCCESS] 查询成功！本次返回 {len(result_list)} 条记录\n")

        # 显示前几条记录
        display_count = min(5, len(result_list))
        if display_count > 0:
            print(f"显示前 {display_count} 条记录：\n")

            for idx, appt in enumerate(result_list[:display_count], 1):
                print(f"[预约 {idx}]")
                print(f"  预约ID: {appt.get('id')}")
                print(f"  学生ID: {appt.get('s_id')}")
                print(f"  教师ID: {appt.get('t_id')}")
                print(f"  开始时间: {appt.get('start_time')}")
                print(f"  结束时间: {appt.get('end_time')}")
                print(f"  状态: {appt.get('status')}")
                print(f"  课程类型: {'英语' if appt.get('course_type') == '1' else '普通话' if appt.get('course_type') == '31' else appt.get('course_type')}")
                print(f"  课程性质: {appt.get('use_point')}")
                print(f"  点数类型: {appt.get('point_type')}")
                print(f"  类别: {appt.get('category')}")
                print(f"  添加时间: {appt.get('add_time')}")
                print()

            if len(result_list) > display_count:
                print(f"... 还有 {len(result_list) - display_count} 条记录未显示\n")

        return {
            'total': total,
            'count': len(result_list),
            'data': result_list
        }

    except Exception as e:
        print(f"[ERROR] 数据库查询异常: {str(e)}")
        import traceback
        traceback.print_exc()
        if conn:
            conn.close()
        return None


def search_user_appointments(stu_id, course_type, start_date=None, end_date=None):
    """
    查询用户约课历史数据

    参数:
        stu_id: 学生ID (必需)
        course_type: 课程类型 (1=英语, 31=普通话)
        start_date: 开始日期，格式 YYYY-MM-DD (可选，默认今天)
        end_date: 结束日期，格式 YYYY-MM-DD (可选，默认今天)

    返回:
        API响应结果
    """
    # API端点
    url = "http://172.16.16.97/talkplatform_timetable_consumer/v2/student/query_history_timetable"

    # 默认日期为今天
    if not start_date:
        start_date = datetime.now().strftime('%Y-%m-%d')
    if not end_date:
        end_date = start_date

    # 生成时间戳（毫秒级）
    timestamp = int(time.time() * 1000)

    # 组装请求参数
    params = {
        'stu_id': str(stu_id),
        'course_type': str(course_type),
        'start_date': start_date,
        'end_date': end_date,
        'appkey': 'crm',
        'timestamp': str(timestamp)
    }

    print(f"\n{'='*60}")
    print(f"查询用户约课数据")
    print(f"{'='*60}")
    print(f"学生ID: {stu_id}")
    print(f"课程类型: {'英语' if course_type == '1' else '普通话' if course_type == '31' else course_type}")
    print(f"查询日期: {start_date} 至 {end_date}")
    print(f"请求参数: {json.dumps(params, ensure_ascii=False)}")
    print(f"{'='*60}\n")

    # 发送GET请求
    result = send_request_get(url, params)

    if result:
        print("[SUCCESS] 查询成功！")
        print(f"\n响应结果:\n{json.dumps(result, ensure_ascii=False, indent=2)}")

        # 解析并显示预约列表
        if result.get('code') == '10000' and result.get('res'):
            appointments = result.get('res', [])
            print(f"\n找到 {len(appointments)} 条预约记录:\n")

            # 预约状态映射
            status_map = {
                1: '正常',
                2: '已完成',
                3: '已取消',
                4: '教师取消',
                5: '学生缺席',
                6: '教师缺席'
            }

            for idx, appt in enumerate(appointments, 1):
                teacher_info = appt.get('teacher_info', {})
                appoint_status = appt.get('appoint_status', 0)
                status_text = status_map.get(appoint_status, f'未知({appoint_status})')

                print(f"[预约 {idx}]")
                print(f"  预约ID: {appt.get('appoint_id', 'N/A')}")
                print(f"  课程ID: {appt.get('lesson_id', 'N/A')}")
                print(f"  教师ID: {teacher_info.get('tea_id', 'N/A')}")
                print(f"  教师昵称: {teacher_info.get('tea_nick_name', 'N/A')}")
                print(f"  开始时间: {appt.get('start_time', 'N/A')}")
                print(f"  结束时间: {appt.get('end_time', 'N/A')}")
                print(f"  状态: {status_text}")
                print(f"  课程性质: {appt.get('use_point', 'N/A')}")
                print(f"  点数类型: {appt.get('point_type', 'N/A')}")
                print(f"  课程名称: {appt.get('lesson_name_en', appt.get('lesson_name', 'N/A'))}")
                print()
        else:
            print(f"[ERROR] 查询失败或无数据: {result.get('message', '未知错误')}")
    else:
        print("[ERROR] 请求失败，未收到响应")

    return result


def search_date_range(stu_id, course_type, days_back=7):
    """
    查询最近N天的约课数据

    参数:
        stu_id: 学生ID
        course_type: 课程类型
        days_back: 向前查询的天数（默认7天）
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)

    return search_user_appointments(
        stu_id=stu_id,
        course_type=course_type,
        start_date=start_date.strftime('%Y-%m-%d'),
        end_date=end_date.strftime('%Y-%m-%d')
    )


if __name__ == '__main__':
    # ============ 配置参数 ============

    # 学生ID（必填）
    STUDENT_ID = 1587389881

    # 课程类型: '1' = 英语, '31' = 普通话
    COURSE_TYPE = '1'

    # ===================================

    print("\n" + "="*60)
    print("约课数据查询工具")
    print("="*60)
    print("\n请选择查询方式：")
    print("1. 通过API查询（按日期范围）")
    print("2. 通过数据库查询（查询所有记录）")
    print("="*60)

    # 默认使用方式2：数据库查询
    query_mode = 2

    if query_mode == 1:
        # 方式1：API查询，需要指定日期范围
        START_DATE = '2021-07-02'  # 格式: YYYY-MM-DD
        END_DATE = '2026-01-02'    # 格式: YYYY-MM-DD

        result = search_user_appointments(
            stu_id=STUDENT_ID,
            course_type=COURSE_TYPE,
            start_date=START_DATE,
            end_date=END_DATE
        )

    elif query_mode == 2:
        # 方式2：数据库查询，查询所有记录
        result = search_user_appointments_from_db(
            stu_id=STUDENT_ID,
            limit=1000,          # 最多返回1000条
            offset=0,            # 从第0条开始
            course_type=None,    # 不过滤课程类型（查询所有）
            status=None          # 不过滤状态（查询所有）
        )

        if result:
            print(f"\n" + "="*60)
            print(f"查询汇总统计")
            print("="*60)
            print(f"总记录数: {result['total']}")
            print(f"本次返回: {result['count']}")
            print("="*60 + "\n")

    # 其他使用示例：
    # 1. 查询最近7天的数据（API方式）
    # result = search_date_range(stu_id=STUDENT_ID, course_type=COURSE_TYPE, days_back=7)

    # 2. 查询指定课程类型（数据库方式）
    # result = search_user_appointments_from_db(stu_id=STUDENT_ID, course_type='1', limit=100)

    # 3. 查询指定状态（数据库方式）
    # result = search_user_appointments_from_db(stu_id=STUDENT_ID, status='on', limit=100)

    # 4. 分页查询（数据库方式）
    # result = search_user_appointments_from_db(stu_id=STUDENT_ID, limit=50, offset=100)


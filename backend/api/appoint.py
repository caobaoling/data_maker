# 文件: api/appoint_v2.py
# 作者: Claude Code
# 创建日期: 2026/01/09
# 描述: 课程预约相关API - 精简统一版

from flask import Blueprint, request, jsonify
import sys
import os
import logging
import json
import random
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 添加项目根目录以导入common模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from common.api_client import send_request_post
from common.db_connect import create_connection

appoint_bp = Blueprint('appoint', __name__)

# 课程类型配置映射表
COURSE_TYPE_CONFIG = {
    '31': {  # 普通话
        'point_type': 'pthpoint',
        'category_buy': 'ph_buy',
        'category_free': 'ph_free',
        'log_name': '普通话'
    },
    '1': {  # 英语
        'point_type': 'point',
        'category_buy': 'ph_buy',
        'category_free': 'ph_free',
        'log_name': '英语'
    },
    '39': {  # 阿语
        'point_type': 'ar_point',
        'category_buy': 'unkown',
        'category_free': 'unkown',
        'log_name': '阿语'
    }
}

def sync_cocos_book_type(appoint_id):
    """预约使用Cocos教材时，同步更新3个相关数据库表"""
    import time
    conn = None
    try:
        conn = create_connection()
        if not conn:
            logger.error("[Cocos同步] 数据库连接失败")
            return False

        cursor = conn.cursor()

        # 等待热数据表写入，最多重试6次，每次等待5秒
        max_retries = 6
        retry_interval = 5
        for attempt in range(max_retries):
            cursor.execute(
                "SELECT COUNT(*) FROM `talkplatform_timetable`.`teacher_hot_timetable` WHERE `lesson_id` = %s",
                (str(appoint_id),)
            )
            if cursor.fetchone()[0] > 0:
                logger.info(f"[Cocos同步] 热数据表已就绪，第{attempt + 1}次检查")
                break
            logger.info(f"[Cocos同步] 热数据表暂无记录，等待{retry_interval}秒后重试({attempt + 1}/{max_retries})")
            time.sleep(retry_interval)
        else:
            logger.warning(f"[Cocos同步] 等待超时，热数据表仍无记录，跳过前两条更新")

        # 1. 更新 talkplatform_timetable.teacher_hot_timetable
        cursor.execute(
            "UPDATE `talkplatform_timetable`.`teacher_hot_timetable` SET `book_type` = 2 WHERE `lesson_id` = %s",
            (str(appoint_id),)
        )
        logger.info(f"[Cocos同步] teacher_hot_timetable 影响行数: {cursor.rowcount}")
        conn.commit()

        # 2. 更新 talkplatform_timetable.student_hot_timetable
        cursor.execute(
            "UPDATE `talkplatform_timetable`.`student_hot_timetable` SET `book_type` = 2 WHERE `lesson_id` = %s",
            (str(appoint_id),)
        )
        logger.info(f"[Cocos同步] student_hot_timetable 影响行数: {cursor.rowcount}")
        conn.commit()

        # 3. 插入或更新 talkplatform_appoint_reconstruction.appoint_book_type
        cursor.execute(
            """INSERT INTO talkplatform_appoint_reconstruction.appoint_book_type (id, s_id, appoint_id, book_type, operator_id)
               SELECT %s, s_id, %s, 1, 237
               FROM talk.appoint
               WHERE id = %s
               ON DUPLICATE KEY UPDATE book_type = 2""",
            (int(appoint_id), int(appoint_id), int(appoint_id))
        )
        logger.info(f"[Cocos同步] appoint_book_type 影响行数: {cursor.rowcount}")
        conn.commit()

        cursor.close()
        conn.close()

        logger.info(f"[Cocos同步] 成功同步预约ID: {appoint_id}")
        return True

    except Exception as e:
        logger.error(f"[Cocos同步] 失败: {str(e)}", exc_info=True)
        if conn:
            conn.close()
        return False


def sync_appoint_to_tables(params):
    """同步预约数据到 teanew.appoint_aggregation 和 talk.appoint 表"""
    try:
        conn = create_connection()
        if not conn:
            logger.error("[数据同步] 数据库连接失败")
            return False

        cursor = conn.cursor()

        # 1. 同步到 teanew.appoint_aggregation
        insert_sql_teanew = """
            INSERT INTO teanew.appoint_aggregation
            (id, t_id, s_id, date_time, tag_id, start_time, end_time, status, date, time, week, add_time,
             course_id, now_level, appoint_type, point_type, cost_num, teach_type, use_point,
             cancel_operator, use_skype_id, need_oral, course_top_id, course_sub_id, course_type,
             tea_salary, package_id, category, is_overseas, extra)
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_sql_teanew, (
            params['id'], params['t_id'], params['s_id'], params['date_time'],
            params['tag_id'], params['start_time'], params['end_time'], params['status'],
            params['date'], params['time'], params['week'], params['add_time'],
            params['course_id'], params['now_level'], params['appoint_type'],
            params['point_type'], params['cost_num'], params['teach_type'],
            params['use_point'], params['cancel_operator'], params['use_skype_id'],
            params['need_oral'], params['course_top_id'], params['course_sub_id'],
            params['course_type'], params['tea_salary'], params['package_id'],
            params['category'], 0, ''  # is_overseas=0, extra=''
        ))

        # 2. 同步到 talk.appoint
        insert_sql_talk = """
            INSERT INTO talk.appoint
            (id, t_id, s_id, date_time, tag_id, start_time, end_time, status, date, time, week, add_time,
             course_id, now_level, appoint_type, point_type, cost_num, teach_type, use_point,
             cancel_operator, use_skype_id, need_oral, course_top_id, course_sub_id, course_type,
             tea_salary, package_id, category)
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_sql_talk, (
            params['id'], params['t_id'], params['s_id'], params['date_time'],
            params['tag_id'], params['start_time'], params['end_time'], params['status'],
            params['date'], params['time'], params['week'], params['add_time'],
            params['course_id'], params['now_level'], params['appoint_type'],
            params['point_type'], params['cost_num'], params['teach_type'],
            params['use_point'], params['cancel_operator'], params['use_skype_id'],
            params['need_oral'], params['course_top_id'], params['course_sub_id'],
            params['course_type'], params['tea_salary'], params['package_id'],
            params['category']
        ))

        conn.commit()
        cursor.close()
        conn.close()

        logger.info(f"[数据同步] 成功同步预约ID: {params['id']}")
        return True

    except Exception as e:
        logger.error(f"[数据同步] 失败: {str(e)}", exc_info=True)
        if conn:
            conn.close()
        return False

def sync_status_to_tables(appoint_id, new_status):
    """同步预约状态到 teanew.appoint_aggregation 和 talk.appoint 表"""
    try:
        conn = create_connection()
        if not conn:
            logger.error("[状态同步] 数据库连接失败")
            return False

        cursor = conn.cursor()

        # 1. 更新 teanew.appoint_aggregation
        update_sql_teanew = """
            UPDATE teanew.appoint_aggregation
            SET status = %s
            WHERE id = %s
        """
        cursor.execute(update_sql_teanew, (new_status, appoint_id))
        rows_affected_teanew = cursor.rowcount

        # 2. 更新 talk.appoint
        update_sql_talk = """
            UPDATE talk.appoint
            SET status = %s
            WHERE id = %s
        """
        cursor.execute(update_sql_talk, (new_status, appoint_id))
        rows_affected_talk = cursor.rowcount

        conn.commit()
        cursor.close()
        conn.close()

        logger.info(f"[状态同步] 成功同步预约ID: {appoint_id}, 状态: {new_status}, "
                   f"teanew影响行数: {rows_affected_teanew}, talk影响行数: {rows_affected_talk}")
        return True

    except Exception as e:
        logger.error(f"[状态同步] 失败: {str(e)}", exc_info=True)
        if conn:
            conn.close()
        return False

@appoint_bp.route('/add', methods=['POST'])
def add_appoint():
    """
    统一添加预约接口
    前端传递 course_type 参数,后端自动识别课程类型并应用对应配置
    """
    try:
        data = request.json

        # 获取课程类型配置
        course_type = str(data.get('course_type', '1'))
        config = COURSE_TYPE_CONFIG.get(course_type, COURSE_TYPE_CONFIG['1'])

        logger.info(f"[{config['log_name']}预约] 收到请求: {json.dumps(data, ensure_ascii=False)}")

        # 计算时间参数
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        start_dt = datetime.strptime(data.get('start_time'), '%Y-%m-%d %H:%M:%S')
        date = start_dt.strftime('%Y%m%d')
        hour = start_dt.hour
        minute = start_dt.minute
        time_num = hour * 2 + (2 if minute >= 30 else 1)

        # 计算 category 和 point_type
        use_point = data.get('use_point', 'buy')
        category = data.get('category') or (config[f'category_{use_point}'])
        point_type = data.get('point_type') or config['point_type']

        # 组装API参数
        params = {
            'id': random.randint(171605105, 971605105),
            's_id': int(data.get('stu_id')),
            't_id': int(data.get('t_id')),
            'tag_id': '87703151451772984942',
            'start_time': data.get('start_time'),
            'end_time': data.get('end_time'),
            'date_time': data.get('date_time'),
            'status': data.get('status', 'on'),
            'date': date,
            'time': time_num,
            'week': '0',
            'add_time': current_time,
            'course_id': str(data.get('course_id')),
            'now_level': '0',
            'appoint_type': 'ios',
            'point_type': point_type,
            'cost_num': str(data.get('cost_num', 1)),
            'teach_type': '51TalkAC',
            'use_point': use_point,
            'cancel_operator': '0',
            'use_skype_id': '0',
            'need_oral': '0',
            'course_top_id': str(data.get('level_id')),
            'course_sub_id': str(data.get('unit_id')),
            'course_type': course_type,
            'tea_salary': '0',
            'package_id': '0',
            'category': category
        }

        logger.info(f"[{config['log_name']}预约] 调用外部API: {json.dumps(params, ensure_ascii=False)}")

        # 调用预约API
        result = send_request_post(
            'http://172.16.16.97/talkplatform_appointone_consumer/v1/appoint/add',
            params
        )

        logger.info(f"[{config['log_name']}预约] API响应: {json.dumps(result, ensure_ascii=False)}")

        # 如果成功，同步数据到其他表
        if result.get('code') == '10000':
            sync_success = sync_appoint_to_tables(params)
            if sync_success:
                logger.info(f"[{config['log_name']}预约] 数据同步成功")
            else:
                logger.warning(f"[{config['log_name']}预约] 数据同步失败(主流程成功)")

            # Cocos教材特殊处理：后台线程异步同步，避免阻塞请求
            book_type = str(data.get('book_type', '1'))
            if book_type == '2':
                import threading
                real_appoint_id = result.get('res', {}).get('id') or params['id']
                thread = threading.Thread(target=sync_cocos_book_type, args=(real_appoint_id,))
                thread.daemon = True
                thread.start()
                logger.info(f"[{config['log_name']}预约] Cocos教材同步已在后台启动，appoint_id: {real_appoint_id}")

        return jsonify(result)

    except Exception as e:
        logger.error(f"[添加预约] 异常: {str(e)}", exc_info=True)
        return jsonify({
            'code': '50000',
            'message': f'请求失败: {str(e)}',
            'data': None
        }), 500

# ========== 以下为其他原有接口(保持不变) ==========

@appoint_bp.route('/textbooks', methods=['GET'])
def get_textbooks():
    """获取教材数据 - 三级联动"""
    try:
        query_type = request.args.get('type', 'level')
        data_dir = os.path.join(os.path.dirname(__file__), '../data')

        if query_type == 'level':
            level_file = os.path.join(data_dir, '教材级别列表.json')
            with open(level_file, 'r', encoding='utf-8') as f:
                levels = json.load(f)
            return jsonify({'code': '10000', 'message': '查询成功', 'data': levels})

        elif query_type == 'units':
            top_id = request.args.get('top_id')
            if not top_id:
                return jsonify({'code': '40000', 'message': '缺少top_id参数'}), 400
            units_file = os.path.join(data_dir, '教材单元列表.json')
            with open(units_file, 'r', encoding='utf-8') as f:
                all_units = json.load(f)
            for item in all_units:
                if item['current_top_id'] == str(top_id):
                    return jsonify({'code': '10000', 'message': '查询成功', 'data': item['units']})
            return jsonify({'code': '10000', 'message': '查询成功', 'data': []})

        elif query_type == 'lessons':
            sub_id = request.args.get('sub_id')
            if not sub_id:
                return jsonify({'code': '40000', 'message': '缺少sub_id参数'}), 400
            conn = create_connection()
            if not conn:
                return jsonify({'code': '50000', 'message': '数据库连接失败'}), 500
            try:
                cursor = conn.cursor()
                sql = "SELECT id, name_zh_cn FROM textbook.series_textbook WHERE tree_parent_id = %s AND tg = 'on' ORDER BY id"
                cursor.execute(sql, (sub_id,))
                rows = cursor.fetchall()
                lessons = [{'id': str(row[0]), 'lesson_name': row[1]} for row in rows]
                cursor.close()
                conn.close()
                return jsonify({'code': '10000', 'message': '查询成功', 'data': lessons})
            except Exception as e:
                if conn:
                    conn.close()
                return jsonify({'code': '50000', 'message': f'查询失败: {str(e)}'}), 500

        return jsonify({'code': '40000', 'message': f'无效查询类型: {query_type}'}), 400

    except Exception as e:
        logger.error(f"[教材查询] 异常: {str(e)}", exc_info=True)
        return jsonify({'code': '50000', 'message': f'请求失败: {str(e)}'}), 500

@appoint_bp.route('/list', methods=['GET'])
def get_appoint_list():
    """查询预约列表"""
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 20))

        # 限制每次查询最多100条，避免数据库压力
        max_limit = 100
        if page_size > max_limit:
            page_size = max_limit

        conditions = []

        # 特殊处理阿语课查询：前端传递 unkown_free 或 unkown_buy
        # 需要同时判断 category='unkown' 和 course_type='39'
        category_param = request.args.get('category')
        if category_param == 'unkown_free':
            conditions.append("category = 'unkown' AND use_point = 'free' AND course_type = '39'")
        elif category_param == 'unkown_buy':
            conditions.append("category = 'unkown' AND use_point = 'buy' AND course_type = '39'")
        elif category_param:
            conditions.append(f"category = '{category_param}'")

        # 处理其他查询条件
        for field, param in [('id', 'appointId'), ('s_id', 'stuId'), ('t_id', 'tId'),
                             ('course_id', 'courseId'), ('status', 'status'),
                             ('course_type', 'courseType')]:
            value = request.args.get(param)
            if value:
                conditions.append(f"{field} = '{value}'" if param in ('appointId', 'courseId', 'status') else f"{field} = {value}")

        start_date = request.args.get('startDate')
        end_date = request.args.get('endDate')
        if start_date:
            conditions.append(f"start_time >= '{start_date} 00:00:00'")
        if end_date:
            conditions.append(f"start_time <= '{end_date} 23:59:59'")

        where_clause = " AND ".join(conditions) if conditions else "1=1"

        conn = create_connection()
        if not conn:
            return jsonify({'code': '50000', 'message': '数据库连接失败'}), 500

        try:
            cursor = conn.cursor()

            # 判断是否有具体查询条件（非空查询）
            has_conditions = where_clause != "1=1"

            # 只在有查询条件时才计算真实总数，否则限制为100避免全表扫描
            if has_conditions:
                cursor.execute(f"SELECT COUNT(*) FROM talkplatform_appoint_reconstruction.appoint WHERE {where_clause}")
                total = cursor.fetchone()[0]
                # 即使有条件，也限制最大显示总数为500
                total = min(total, 500)
            else:
                # 无查询条件时，设置总数为100，提示用户添加查询条件
                total = 100
                logger.warning("[预约列表] 无查询条件，限制返回100条数据")

            offset = (page - 1) * page_size
            sql = f"""SELECT id, s_id, t_id, start_time, end_time, status, course_type, point_type, use_point, category,
                      course_id, course_top_id as level_id, course_sub_id as unit_id, add_time, date_time, date, time
                      FROM talkplatform_appoint_reconstruction.appoint WHERE {where_clause}
                      ORDER BY start_time DESC LIMIT {page_size} OFFSET {offset}"""
            cursor.execute(sql)

            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            result_list = []
            for row in rows:
                item = dict(zip(columns, row))
                for time_field in ['start_time', 'end_time', 'add_time']:
                    if item.get(time_field):
                        item[time_field] = str(item[time_field])
                result_list.append(item)

            cursor.close()
            conn.close()

            return jsonify({'code': '10000', 'message': '查询成功',
                           'data': {'list': result_list, 'total': total, 'page': page, 'pageSize': page_size}})
        except Exception as e:
            if conn:
                conn.close()
            return jsonify({'code': '50000', 'message': f'查询失败: {str(e)}'}), 500

    except Exception as e:
        return jsonify({'code': '50000', 'message': f'请求失败: {str(e)}'}), 500

@appoint_bp.route('/update_status', methods=['POST'])
def update_appoint_status():
    """修改预约状态"""
    try:
        data = request.json
        appoint_id = data.get('id')
        new_status = data.get('status')

        if not appoint_id or not new_status:
            return jsonify({'code': '40000', 'message': '预约ID和状态不能为空'}), 400

        valid_statuses = ['on', 'end', 's_absent', 't_absent', 'cancel']
        if new_status not in valid_statuses:
            return jsonify({'code': '40000', 'message': f'无效状态值'}), 400

        import time
        stamp_time = int(time.time())
        api_params = {'id': str(appoint_id), 'status': new_status,
                     'cancel_time': stamp_time, 'update_time': stamp_time}

        logger.info(f"[状态变更] 预约ID: {appoint_id}, 新状态: {new_status}")

        result = send_request_post(
            'http://172.16.16.97/talkplatform_appointone_consumer/v1/appoint/update',
            api_params
        )

        logger.info(f"[状态变更] API响应: {json.dumps(result, ensure_ascii=False)}")

        # 如果外部API调用成功，同步状态到其他表
        if result.get('code') == '10000':
            sync_success = sync_status_to_tables(appoint_id, new_status)
            if sync_success:
                logger.info(f"[状态变更] 状态同步成功")
            else:
                logger.warning(f"[状态变更] 状态同步失败(主流程成功)")

        return jsonify(result)

    except Exception as e:
        logger.error(f"[状态变更] 异常: {str(e)}", exc_info=True)
        return jsonify({'code': '50000', 'message': f'请求失败: {str(e)}'}), 500

@appoint_bp.route('/sync_cocos', methods=['POST'])
def sync_cocos():
    """手动触发Cocos教材数据库同步"""
    try:
        data = request.json
        appoint_id = data.get('appoint_id')
        if not appoint_id:
            return jsonify({'code': '40000', 'message': '预约ID不能为空'}), 400

        success = sync_cocos_book_type(appoint_id)
        if success:
            return jsonify({'code': '10000', 'message': '同步成功'})
        else:
            return jsonify({'code': '50000', 'message': '同步失败，请查看后端日志'})
    except Exception as e:
        logger.error(f"[Cocos手动同步] 异常: {str(e)}", exc_info=True)
        return jsonify({'code': '50000', 'message': f'请求失败: {str(e)}'}), 500


@appoint_bp.route('/add_star', methods=['POST'])
def add_appoint_star():
    """给预约打星"""
    try:
        data = request.json
        stu_id = data.get('stu_id')
        appoint_id = data.get('appoint_id')
        star_num = data.get('star_num', 5)

        if not stu_id or not appoint_id:
            return jsonify({'code': '40000', 'message': '学生ID和预约ID不能为空'}), 400
        if not (1 <= star_num <= 5):
            return jsonify({'code': '40000', 'message': '星数必须在1-5之间'}), 400

        import time
        import requests
        timestamp = int(time.time())

        params = {
            'biz_category': 'game_system',
            'tsign': 'F72C2788F98F1555779C59FC4AF34D94',
            'talk_token': 'bl%7CjnoQqt-nkHuy0pvsReULc0WZDgxh9SNxVuf7nCAQTtJ3IeGNvBsX1NDzU4x7TZCaDbaob7AdwCGbsUc6Fs5EZDX9%2FUM2CXmRf0RnP3A%3D',
            'userId': stu_id, 'stu_id': stu_id, 'star_num': star_num, 'appoint_id': appoint_id,
            'resolution': '2560_1600', 'physics_size': '10.8', 'device_mod': 'MRX-AL09&oaid=efd76ff9-f9e5-90e4-8dd7-dc9f7f5f209c',
            'device_firm': 'HUAWEI', 'client_id': '86794e128dccc9646eb48883e7880655',
            'appkey': 'junior_app', 'phoneType': 'andrKid', 'deviceType': 'HUAWEI_MRX-AL09',
            'deviceId': '6281638E49D54D7384A70EEA736E1F88', 'systemVer': '31', 'channel': 'hicloud',
            'version': '6.1.7', 'timestamp': timestamp, 'task_biz_category_list': 'elf_week_task,elf_month_task'
        }

        response = requests.get('https://appi.51talkglobal.com/User/sendStar', params=params, timeout=10)

        if response.status_code == 200:
            return jsonify({'code': '10000', 'message': '打星成功', 'data': response.json()})
        else:
            return jsonify({'code': '50000', 'message': f'打星失败: HTTP {response.status_code}'}), 500

    except Exception as e:
        logger.error(f"[预约打星] 异常: {str(e)}", exc_info=True)
        return jsonify({'code': '50000', 'message': f'请求失败: {str(e)}'}), 500

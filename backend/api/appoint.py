# 文件: api/appoint.py
# 作者: Claude Code
# 创建日期: 2026/01/09
# 描述: 课程预约相关API - 简化版(无验证)

from flask import Blueprint, request, jsonify
import sys
import os
import logging
import json

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 添加项目根目录以导入common模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from common.api_client import send_request_post

appoint_bp = Blueprint('appoint', __name__)

@appoint_bp.route('/add_cn', methods=['POST'])
def add_appoint_cn():
    """
    添加普通话预约 (无验证版本)
    直接使用前端传来的数据，不做验证
    """
    try:
        data = request.json
        logger.info(f"[普通话预约] 收到前端请求数据: {json.dumps(data, ensure_ascii=False)}")

        # 导入必需的模块
        import random
        from datetime import datetime

        # 生成必需的参数
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        start_dt = datetime.strptime(data.get('start_time'), '%Y-%m-%d %H:%M:%S')
        date = start_dt.strftime('%Y%m%d')
        hour = start_dt.hour
        minute = start_dt.minute
        time_num = hour * 2 + (2 if minute >= 30 else 1)

        # 计算 category
        use_point = data.get('use_point', 'buy')
        category = f"ph_{use_point}"

        # 组装完整的API参数（按照原始脚本的格式）
        params = {
            'id': random.randint(171605105, 971605105),  # 随机ID
            's_id': int(data.get('stu_id')),  # 注意：原始API使用 s_id 不是 stu_id
            't_id': int(data.get('t_id')),
            'tag_id': '87703151451772984942',  # 固定值
            'start_time': data.get('start_time'),
            'end_time': data.get('end_time'),
            'date_time': data.get('date_time'),
            'status': data.get('status', 'on'),
            'date': date,
            'time': time_num,
            'week': '0',
            'add_time': current_time,
            'course_id': str(data.get('course_id', '1001')),
            'now_level': '0',
            'appoint_type': 'ios',
            'point_type': data.get('point_type', 'pthpoint'),
            'cost_num': '1',
            'teach_type': '51TalkAC',
            'use_point': use_point,
            'cancel_operator': '0',
            'use_skype_id': '0',
            'need_oral': '0',
            'course_top_id': str(data.get('course_top_id', '100')),
            'course_sub_id': str(data.get('course_sub_id', '10')),
            'course_type': str(data.get('course_type', '31')),
            'tea_salary': '0',
            'package_id': '0',
            'category': category
        }

        logger.info(f"[普通话预约] 向外部API发送参数: {json.dumps(params, ensure_ascii=False)}")

        # 调用现有API
        result = send_request_post(
            'http://172.16.16.97/talkplatform_appointone_consumer/v1/appoint/add',
            params
        )

        logger.info(f"[普通话预约] 外部API响应: {json.dumps(result, ensure_ascii=False)}")
        return jsonify(result)

    except Exception as e:
        logger.error(f"[普通话预约] 异常: {str(e)}", exc_info=True)
        return jsonify({
            'code': '50000',
            'message': f'请求失败: {str(e)}',
            'data': None
        }), 500

@appoint_bp.route('/add_en', methods=['POST'])
def add_appoint_en():
    """
    添加英语预约 (无验证版本)
    """
    try:
        data = request.json
        logger.info(f"[英语预约] 收到前端请求数据: {json.dumps(data, ensure_ascii=False)}")

        # 导入必需的模块
        import random
        from datetime import datetime

        # 生成必需的参数
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        start_dt = datetime.strptime(data.get('start_time'), '%Y-%m-%d %H:%M:%S')
        date = start_dt.strftime('%Y%m%d')
        hour = start_dt.hour
        minute = start_dt.minute
        time_num = hour * 2 + (2 if minute >= 30 else 1)

        # 计算 category（英语课用 en_ 前缀）
        use_point = data.get('use_point', 'buy')
        category = f"en_{use_point}"

        # 组装完整的API参数（按照原始脚本的格式）
        params = {
            'id': random.randint(171605105, 971605105),  # 随机ID
            's_id': int(data.get('stu_id')),  # 注意：原始API使用 s_id 不是 stu_id
            't_id': int(data.get('t_id')),
            'tag_id': '87703151451772984942',  # 固定值
            'start_time': data.get('start_time'),
            'end_time': data.get('end_time'),
            'date_time': data.get('date_time'),
            'status': data.get('status', 'on'),
            'date': date,
            'time': time_num,
            'week': '0',
            'add_time': current_time,
            'course_id': str(data.get('course_id', '1001')),
            'now_level': '0',
            'appoint_type': 'ios',
            'point_type': data.get('point_type', 'point'),
            'cost_num': '1',
            'teach_type': '51TalkAC',
            'use_point': use_point,
            'cancel_operator': '0',
            'use_skype_id': '0',
            'need_oral': '0',
            'course_top_id': str(data.get('course_top_id', '100')),
            'course_sub_id': str(data.get('course_sub_id', '10')),
            'course_type': str(data.get('course_type', '1')),
            'tea_salary': '0',
            'package_id': '0',
            'category': category
        }

        logger.info(f"[英语预约] 向外部API发送参数: {json.dumps(params, ensure_ascii=False)}")

        # 调用现有API
        result = send_request_post(
            'http://172.16.16.97/talkplatform_appointone_consumer/v1/appoint/add',
            params
        )

        logger.info(f"[英语预约] 外部API响应: {json.dumps(result, ensure_ascii=False)}")
        return jsonify(result)

    except Exception as e:
        logger.error(f"[英语预约] 异常: {str(e)}", exc_info=True)
        return jsonify({
            'code': '50000',
            'message': f'请求失败: {str(e)}',
            'data': None
        }), 500

@appoint_bp.route('/list', methods=['GET'])
def get_appoint_list():
    """
    查询预约列表
    支持分页和筛选
    """
    try:
        # 导入数据库模块
        import sys
        import os
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
        from common.db_connect import create_connection, select_data

        # 获取查询参数
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 20))
        stu_id = request.args.get('stuId', '')
        t_id = request.args.get('tId', '')
        status = request.args.get('status', '')
        course_type = request.args.get('courseType', '')
        category = request.args.get('category', '')
        start_date = request.args.get('startDate', '')
        end_date = request.args.get('endDate', '')

        logger.info(f"[预约列表] 查询参数 - page:{page}, pageSize:{page_size}, stuId:{stu_id}, tId:{t_id}, category:{category}")

        # 构建查询条件
        conditions = []
        if stu_id:
            conditions.append(f"s_id = {stu_id}")
        if t_id:
            conditions.append(f"t_id = {t_id}")
        if status:
            conditions.append(f"status = '{status}'")
        if course_type:
            conditions.append(f"course_type = '{course_type}'")
        if category:
            conditions.append(f"category = '{category}'")
        if start_date:
            conditions.append(f"start_time >= '{start_date} 00:00:00'")
        if end_date:
            conditions.append(f"start_time <= '{end_date} 23:59:59'")

        where_clause = " AND ".join(conditions) if conditions else "1=1"

        # 连接数据库
        conn = create_connection()
        if not conn:
            return jsonify({
                'code': '50000',
                'message': '数据库连接失败',
                'data': None
            }), 500

        try:
            # 查询总数
            cursor = conn.cursor()
            count_sql = f"SELECT COUNT(*) as total FROM talkplatform_appoint_reconstruction.appoint WHERE {where_clause}"
            cursor.execute(count_sql)
            total = cursor.fetchone()[0]

            # 查询列表数据
            offset = (page - 1) * page_size
            list_sql = f"""
                SELECT
                    id, s_id, t_id, start_time, end_time, status,
                    course_type, point_type, use_point, category,
                    course_id, course_top_id, course_sub_id,
                    add_time, date_time, date, time
                FROM talkplatform_appoint_reconstruction.appoint
                WHERE {where_clause}
                ORDER BY id DESC
                LIMIT {page_size} OFFSET {offset}
            """
            cursor.execute(list_sql)

            # 获取列名
            columns = [desc[0] for desc in cursor.description]

            # 转换为字典列表
            rows = cursor.fetchall()
            result_list = []
            for row in rows:
                item = dict(zip(columns, row))
                # 转换时间格式
                if item.get('start_time'):
                    item['start_time'] = str(item['start_time'])
                if item.get('end_time'):
                    item['end_time'] = str(item['end_time'])
                if item.get('add_time'):
                    item['add_time'] = str(item['add_time'])
                result_list.append(item)

            cursor.close()
            conn.close()

            logger.info(f"[预约列表] 查询成功 - 共{total}条记录，返回第{page}页")

            return jsonify({
                'code': '10000',
                'message': '查询成功',
                'data': {
                    'list': result_list,
                    'total': total,
                    'page': page,
                    'pageSize': page_size
                }
            })

        except Exception as e:
            logger.error(f"[预约列表] 数据库查询异常: {str(e)}", exc_info=True)
            if conn:
                conn.close()
            return jsonify({
                'code': '50000',
                'message': f'数据库查询失败: {str(e)}',
                'data': None
            }), 500

    except Exception as e:
        logger.error(f"[预约列表] 异常: {str(e)}", exc_info=True)
        return jsonify({
            'code': '50000',
            'message': f'请求失败: {str(e)}',
            'data': None
        }), 500

@appoint_bp.route('/update_status', methods=['POST'])
def update_appoint_status():
    """
    修改预约状态
    """
    try:
        data = request.json
        appoint_id = data.get('id')
        new_status = data.get('status')

        logger.info(f"[状态变更] 预约ID:{appoint_id}, 新状态:{new_status}")

        if not appoint_id or not new_status:
            return jsonify({
                'code': '40000',
                'message': '预约ID和状态不能为空',
                'data': None
            }), 400

        # 验证状态值
        valid_statuses = ['on', 'end', 's_absent', 't_absent', 'cancel']
        if new_status not in valid_statuses:
            return jsonify({
                'code': '40000',
                'message': f'无效的状态值，允许的值: {", ".join(valid_statuses)}',
                'data': None
            }), 400

        # 连接数据库
        import sys
        import os
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
        from common.db_connect import create_connection

        conn = create_connection()
        if not conn:
            return jsonify({
                'code': '50000',
                'message': '数据库连接失败',
                'data': None
            }), 500

        try:
            cursor = conn.cursor()

            # 更新状态
            update_sql = f"""
                UPDATE talkplatform_appoint_reconstruction.appoint
                SET status = '{new_status}'
                WHERE id = {appoint_id}
            """
            cursor.execute(update_sql)
            conn.commit()

            affected_rows = cursor.rowcount
            cursor.close()
            conn.close()

            if affected_rows > 0:
                logger.info(f"[状态变更] 成功 - 预约ID:{appoint_id}, 新状态:{new_status}")
                return jsonify({
                    'code': '10000',
                    'message': '状态修改成功',
                    'data': {'id': appoint_id, 'status': new_status}
                })
            else:
                logger.warning(f"[状态变更] 失败 - 预约ID:{appoint_id}不存在")
                return jsonify({
                    'code': '40000',
                    'message': '预约记录不存在',
                    'data': None
                }), 404

        except Exception as e:
            logger.error(f"[状态变更] 数据库操作异常: {str(e)}", exc_info=True)
            if conn:
                conn.rollback()
                conn.close()
            return jsonify({
                'code': '50000',
                'message': f'数据库操作失败: {str(e)}',
                'data': None
            }), 500

    except Exception as e:
        logger.error(f"[状态变更] 异常: {str(e)}", exc_info=True)
        return jsonify({
            'code': '50000',
            'message': f'请求失败: {str(e)}',
            'data': None
        }), 500

@appoint_bp.route('/add_star', methods=['POST'])
def add_appoint_star():
    """
    给预约添加星星评价
    """
    try:
        data = request.json
        stu_id = data.get('stu_id')
        appoint_id = data.get('appoint_id')
        star_num = data.get('star_num', 5)

        logger.info(f"[预约打星] 学生ID:{stu_id}, 预约ID:{appoint_id}, 星数:{star_num}")

        if not stu_id or not appoint_id:
            return jsonify({
                'code': '40000',
                'message': '学生ID和预约ID不能为空',
                'data': None
            }), 400

        # 验证星数范围
        if not (1 <= star_num <= 5):
            return jsonify({
                'code': '40000',
                'message': '星数必须在1-5之间',
                'data': None
            }), 400

        # 导入必需的模块
        import time

        # 生成时间戳
        timestamp = int(time.time())

        # 调用外部打星API
        api_url = 'https://appi.51talkglobal.com/User/sendStar'
        params = {
            'biz_category': 'game_system',
            'tsign': 'F72C2788F98F1555779C59FC4AF34D94',
            'talk_token': 'bl%7CjnoQqt-nkHuy0pvsReULc0WZDgxh9SNxVuf7nCAQTtJ3IeGNvBsX1NDzU4x7TZCaDbaob7AdwCGbsUc6Fs5EZDX9%2FUM2CXmRf0RnP3A%3D',
            'userId': stu_id,
            'stu_id': stu_id,
            'star_num': star_num,
            'resolution': '2560_1600',
            'physics_size': '10.8',
            'device_mod': 'MRX-AL09&oaid=efd76ff9-f9e5-90e4-8dd7-dc9f7f5f209c',
            'device_firm': 'HUAWEI',
            'client_id': '86794e128dccc9646eb48883e7880655',
            'appoint_id': appoint_id,
            'appkey': 'junior_app',
            'phoneType': 'andrKid',
            'deviceType': 'HUAWEI_MRX-AL09',
            'deviceId': '6281638E49D54D7384A70EEA736E1F88',
            'systemVer': '31',
            'channel': 'hicloud',
            'version': '6.1.7',
            'timestamp': timestamp,
            'task_biz_category_list': 'elf_week_task,elf_month_task'
        }

        logger.info(f"[预约打星] 调用外部API: {api_url}")

        # 发送请求
        import requests
        response = requests.get(api_url, params=params, timeout=10)

        if response.status_code == 200:
            result = response.json()
            logger.info(f"[预约打星] 外部API响应: {json.dumps(result, ensure_ascii=False)}")

            # 返回外部API的响应
            return jsonify({
                'code': '10000',
                'message': '打星成功',
                'data': result
            })
        else:
            logger.error(f"[预约打星] 外部API请求失败: status={response.status_code}, response={response.text}")
            return jsonify({
                'code': '50000',
                'message': f'打星请求失败: HTTP {response.status_code}',
                'data': None
            }), 500

    except Exception as e:
        logger.error(f"[预约打星] 异常: {str(e)}", exc_info=True)
        return jsonify({
            'code': '50000',
            'message': f'请求失败: {str(e)}',
            'data': None
        }), 500

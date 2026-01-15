# 文件: api/elf.py
# 作者: Claude Code
# 创建日期: 2026/01/14
# 描述: 精灵系统管理工具API

from flask import Blueprint, request, jsonify
import sys
import os
import logging
import time
import requests
from datetime import datetime, timedelta
import datetime as dt

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 添加项目根目录以导入common模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from common.db_connect import create_connection, execute_query
from common.execute_batch import execute_batch_op
from common.elf_level_config import ElfLevelData

elf_bp = Blueprint('elf', __name__)


@elf_bp.route('/add_star', methods=['POST'])
def add_star():
    """
    给课程添加星星
    参数:
        user_id: 用户ID (必填)
        appoint_id: 预约ID (必填)
        star_num: 星星数量 (可选，默认2)
    """
    try:
        data = request.json
        user_id = data.get('user_id')
        appoint_id = data.get('appoint_id')
        star_num = data.get('star_num', 2)

        if not user_id:
            return jsonify({
                'code': '400',
                'msg': '用户ID不能为空',
                'data': None
            }), 400

        if not appoint_id:
            return jsonify({
                'code': '400',
                'msg': '预约ID不能为空',
                'data': None
            }), 400

        logger.info(f"[添加星星] 用户ID: {user_id}, 预约ID: {appoint_id}, 星星数: {star_num}")

        # 调用第三方API
        api_url = 'https://appi.51talkglobal.com/User/sendStar'

        timestamp_seconds = int(time.time())

        params = {
            'biz_category': 'game_system',
            'tsign': 'F72C2788F98F1555779C59FC4AF34D94',
            'talk_token': 'bl%7CjnoQqt-nkHuy0pvsReULc0WZDgxh9SNxVuf7nCAQTtJ3IeGNvBsX1NDzU4x7TZCaDbaob7AdwCGbsUc6Fs5EZDX9%2FUM2CXmRf0RnP3A%3D',
            'userId': user_id,
            'stu_id': user_id,
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
            'timestamp': timestamp_seconds,
            'task_biz_category_list': 'elf_week_task,elf_month_task'
        }

        response = requests.get(api_url, params=params, timeout=10)

        if response.status_code == 200:
            try:
                result = response.json()
                # 第三方API返回的code可能是字符串'10000'或数字10000
                if str(result.get('code')) == '10000':
                    logger.info(f"[添加星星] 成功，响应: {result}")
                    return jsonify({
                        'code': '0',
                        'msg': '添加星星成功',
                        'data': {
                            'user_id': user_id,
                            'appoint_id': appoint_id,
                            'star_num': star_num,
                            'result': result
                        }
                    })
                else:
                    # 获取错误信息，确保返回字符串
                    error_msg = result.get('message') or result.get('msg') or '添加失败'
                    if isinstance(error_msg, dict):
                        error_msg = '添加失败'
                    return jsonify({
                        'code': '500',
                        'msg': error_msg,
                        'data': result
                    }), 500
            except Exception as e:
                logger.error(f"[添加星星] 解析响应失败: {e}")
                return jsonify({
                    'code': '500',
                    'msg': f'解析响应失败: {str(e)}',
                    'data': {'response_text': response.text}
                }), 500
        else:
            logger.error(f"[添加星星] 失败，状态码: {response.status_code}")
            return jsonify({
                'code': '500',
                'msg': f'请求失败，状态码: {response.status_code}',
                'data': None
            }), 500

    except requests.exceptions.Timeout:
        logger.error(f"[添加星星] 请求超时")
        return jsonify({
            'code': '500',
            'msg': '请求超时',
            'data': None
        }), 500
    except Exception as e:
        logger.error(f"[添加星星] 错误: {e}")
        return jsonify({
            'code': '500',
            'msg': f'添加失败: {str(e)}',
            'data': None
        }), 500


@elf_bp.route('/change_level', methods=['POST'])
def change_level():
    """
    修改精灵等级
    参数:
        user_id: 用户ID (必填)
        level: 目标等级 (必填, 1-10)
    """
    try:
        data = request.json
        user_id = data.get('user_id')
        level = data.get('level')

        if not user_id:
            return jsonify({
                'code': '400',
                'msg': '用户ID不能为空',
                'data': None
            }), 400

        if not level:
            return jsonify({
                'code': '400',
                'msg': '等级不能为空',
                'data': None
            }), 400

        # 获取等级配置数据
        level_data = ElfLevelData.get_level_data(level)

        if not level_data:
            return jsonify({
                'code': '400',
                'msg': f'无效的等级: {level}',
                'data': None
            }), 400

        logger.info(f"[修改精灵等级] 用户ID: {user_id}, 等级: {level}")

        conn = create_connection()
        cursor = conn.cursor()

        try:
            # 更新精灵等级
            update_query = """
                UPDATE `talkplatform_game`.`user_elf`
                SET `elf_total_exp` = %s,
                    `elf_level_exp` = %s,
                    `elf_level` = %s,
                    `elf_style_code` = %s
                WHERE user_id = %s
            """
            cursor.execute(update_query, (
                level_data['elf_total_exp'],
                level_data['elf_level_exp'],
                level,
                level_data['elf_style_code'],
                user_id
            ))
            conn.commit()

            logger.info(f"[修改精灵等级] 成功更新用户 {user_id} 到等级 {level}")

            return jsonify({
                'code': '0',
                'msg': f'成功将精灵等级修改为 {level}',
                'data': {
                    'user_id': user_id,
                    'level': level,
                    'level_data': level_data
                }
            })

        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        logger.error(f"[修改精灵等级] 错误: {e}")
        return jsonify({
            'code': '500',
            'msg': f'修改失败: {str(e)}',
            'data': None
        }), 500


@elf_bp.route('/query_level', methods=['POST'])
def query_level():
    """
    查询精灵等级
    参数:
        user_id: 用户ID (必填)
    """
    try:
        data = request.json
        user_id = data.get('user_id')

        if not user_id:
            return jsonify({
                'code': '400',
                'msg': '用户ID不能为空',
                'data': None
            }), 400

        logger.info(f"[查询精灵等级] 用户ID: {user_id}")

        conn = create_connection()
        cursor = conn.cursor()

        try:
            # 查询精灵等级信息
            query = """
                SELECT user_id, elf_total_exp, elf_level_exp, elf_level, elf_style_code
                FROM `talkplatform_game`.`user_elf`
                WHERE user_id = %s
            """
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()

            if not result:
                return jsonify({
                    'code': '404',
                    'msg': '未找到该用户的精灵信息',
                    'data': None
                }), 404

            elf_info = {
                'user_id': result[0],
                'elf_total_exp': result[1],
                'elf_level_exp': result[2],
                'elf_level': result[3],
                'elf_style_code': result[4]
            }

            logger.info(f"[查询精灵等级] 用户 {user_id} 当前等级: {elf_info['elf_level']}")

            return jsonify({
                'code': '0',
                'msg': '查询成功',
                'data': elf_info
            })

        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        logger.error(f"[查询精灵等级] 错误: {e}")
        return jsonify({
            'code': '500',
            'msg': f'查询失败: {str(e)}',
            'data': None
        }), 500


@elf_bp.route('/create_endclass', methods=['POST'])
def create_endclass():
    """
    精灵结课
    参数:
        user_id: 用户ID (必填)
        biz_id: 业务ID/约课ID (必填)
    """
    try:
        data = request.json
        user_id = data.get('user_id')
        biz_id = data.get('biz_id')

        if not user_id:
            return jsonify({
                'code': '400',
                'msg': '用户ID不能为空',
                'data': None
            }), 400

        if not biz_id:
            return jsonify({
                'code': '400',
                'msg': '业务ID不能为空',
                'data': None
            }), 400

        logger.info(f"[精灵结课] 用户ID: {user_id}, 业务ID: {biz_id}")

        # 调用第三方API
        api_url = 'http://172.16.16.36:10006/talkplatform_game/v1/rank/user_settle'

        timestamp_seconds = int(time.time())

        params = {
            'stu_id': user_id,
            'type': '2',
            'appkey': 'java',
            'timestamp': timestamp_seconds,
            'biz_id': biz_id
        }

        response = requests.post(api_url, json=params, timeout=10)

        if response.status_code == 200:
            try:
                result = response.json()
                if result.get('code') == '10000':
                    logger.info(f"[精灵结课] 成功，响应: {result}")
                    return jsonify({
                        'code': '0',
                        'msg': '精灵结课成功',
                        'data': {
                            'user_id': user_id,
                            'biz_id': biz_id,
                            'result': result
                        }
                    })
                else:
                    return jsonify({
                        'code': '500',
                        'msg': result.get('message', '结课失败'),
                        'data': result
                    }), 500
            except Exception as e:
                logger.error(f"[精灵结课] 解析响应失败: {e}")
                return jsonify({
                    'code': '500',
                    'msg': f'解析响应失败: {str(e)}',
                    'data': {'response_text': response.text}
                }), 500
        else:
            logger.error(f"[精灵结课] 失败，状态码: {response.status_code}")
            return jsonify({
                'code': '500',
                'msg': f'请求失败，状态码: {response.status_code}',
                'data': None
            }), 500

    except requests.exceptions.Timeout:
        logger.error(f"[精灵结课] 请求超时")
        return jsonify({
            'code': '500',
            'msg': '请求超时',
            'data': None
        }), 500
    except Exception as e:
        logger.error(f"[精灵结课] 错误: {e}")
        return jsonify({
            'code': '500',
            'msg': f'结课失败: {str(e)}',
            'data': None
        }), 500


@elf_bp.route('/query_task', methods=['POST'])
def query_task():
    """
    查询精灵任务
    参数:
        user_id: 用户ID (必填)
    """
    try:
        data = request.json
        user_id = data.get('user_id')

        if not user_id:
            return jsonify({
                'code': '400',
                'msg': '用户ID不能为空',
                'data': None
            }), 400

        logger.info(f"[查询精灵任务] 用户ID: {user_id}")

        # 调用第三方API
        api_url = 'http://172.16.16.36/talkplatform_task_consumer/task/user_task/v1/front/query_in_cycle_user_task_list'

        timestamp_seconds = int(time.time())

        params = {
            'biz_category': 'game_system',
            'user_id': user_id,
            'appkey': 'java',
            'timestamp': timestamp_seconds,
            'task_biz_category_list': 'elf_week_task,elf_month_task'
        }

        response = requests.get(api_url, params=params, timeout=10)

        if response.status_code == 200:
            try:
                result = response.json()
                # 转换code为字符串进行比较，避免类型不一致
                code_str = str(result.get('code'))

                if code_str == '10000':
                    logger.info(f"[查询精灵任务] 成功，响应: {result}")
                    return jsonify({
                        'code': '0',
                        'msg': '查询成功',
                        'data': {
                            'user_id': user_id,
                            'tasks': result.get('data', [])
                        }
                    })
                # 处理empty data情况（code='10006'），返回空数组
                elif code_str == '10006' and result.get('message') == 'empty data':
                    logger.info(f"[查询精灵任务] 用户 {user_id} 暂无任务数据")
                    return jsonify({
                        'code': '0',
                        'msg': '查询成功（暂无任务数据）',
                        'data': {
                            'user_id': user_id,
                            'tasks': []
                        }
                    })
                else:
                    # 其他错误码，返回失败
                    error_msg = result.get('message') or result.get('msg') or '查询失败'
                    if isinstance(error_msg, dict):
                        error_msg = '查询失败'
                    return jsonify({
                        'code': '500',
                        'msg': error_msg,
                        'data': result
                    }), 500
            except Exception as e:
                logger.error(f"[查询精灵任务] 解析响应失败: {e}")
                return jsonify({
                    'code': '500',
                    'msg': f'解析响应失败: {str(e)}',
                    'data': {'response_text': response.text}
                }), 500
        else:
            logger.error(f"[查询精灵任务] 失败，状态码: {response.status_code}")
            return jsonify({
                'code': '500',
                'msg': f'请求失败，状态码: {response.status_code}',
                'data': None
            }), 500

    except requests.exceptions.Timeout:
        logger.error(f"[查询精灵任务] 请求超时")
        return jsonify({
            'code': '500',
            'msg': '请求超时',
            'data': None
        }), 500
    except Exception as e:
        logger.error(f"[查询精灵任务] 错误: {e}")
        return jsonify({
            'code': '500',
            'msg': f'查询失败: {str(e)}',
            'data': None
        }), 500


@elf_bp.route('/delete_task', methods=['POST'])
def delete_task():
    """
    删除精灵任务
    参数:
        user_id: 用户ID (必填)
    """
    try:
        data = request.json
        user_id = data.get('user_id')

        if not user_id:
            return jsonify({
                'code': '400',
                'msg': '用户ID不能为空',
                'data': None
            }), 400

        logger.info(f"[删除精灵任务] 用户ID: {user_id}")

        conn = create_connection()
        cursor = conn.cursor()

        try:
            # 查询需要删除的任务ID
            select_query = """
                SELECT id FROM talkplatform_task.user_task
                WHERE user_id = %s AND task_info_id IN (
                    SELECT id FROM talkplatform_task.task_info
                    WHERE biz_category = 'game_system' AND id >= 20935
                )
            """
            cursor.execute(select_query, (user_id,))
            task_ids = cursor.fetchall()

            if not task_ids:
                return jsonify({
                    'code': '0',
                    'msg': '该用户没有需要删除的精灵任务',
                    'data': {
                        'user_id': user_id,
                        'deleted_count': 0
                    }
                })

            deleted_tasks = []
            failed_tasks = []

            # 删除每个任务相关的数据
            for row in task_ids:
                task_id = row[0]
                try:
                    delete_queries = [
                        ("DELETE FROM talkplatform_task.user_task WHERE id = %s", "id"),
                        ("DELETE FROM talkplatform_task.user_task_award WHERE id = %s", "id"),
                        (f"DELETE FROM talkplatform_task.user_task_{int(str(user_id)[-2:])} WHERE id = %s", "id"),
                        ("DELETE FROM talkplatform_task.user_task_process_record WHERE user_task_id = %s", "user_task_id"),
                        ("DELETE FROM talkplatform_task.user_award WHERE user_task_id = %s", "user_task_id"),
                        (f"DELETE FROM talkplatform_task.user_award_{int(str(user_id)[-2:])} WHERE user_task_id = %s", "user_task_id")
                    ]

                    execute_batch_op(conn, delete_queries, task_id)
                    deleted_tasks.append(task_id)
                    logger.info(f"[删除精灵任务] 成功删除任务ID: {task_id}")
                except Exception as e:
                    failed_tasks.append({'task_id': task_id, 'error': str(e)})
                    logger.error(f"[删除精灵任务] 删除任务ID {task_id} 失败: {e}")

            logger.info(f"[删除精灵任务] 用户 {user_id} 删除完成，成功 {len(deleted_tasks)} 个，失败 {len(failed_tasks)} 个")

            return jsonify({
                'code': '0',
                'msg': f'成功删除 {len(deleted_tasks)} 个任务',
                'data': {
                    'user_id': user_id,
                    'deleted_count': len(deleted_tasks),
                    'failed_count': len(failed_tasks),
                    'deleted_tasks': deleted_tasks,
                    'failed_tasks': failed_tasks
                }
            })

        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        logger.error(f"[删除精灵任务] 错误: {e}")
        return jsonify({
            'code': '500',
            'msg': f'删除失败: {str(e)}',
            'data': None
        }), 500


@elf_bp.route('/manage_rank', methods=['POST'])
def manage_rank():
    """
    管理精灵排行榜
    功能: 删除上周排行榜数据 + 重置机器人和用户状态
    参数: 无（自动计算上周时间）
    """
    try:
        # 计算上周的时间键
        today = dt.date.today()
        days_to_sunday = 7 - today.isoweekday()
        if days_to_sunday == 7:
            days_to_sunday = 0
        current_sunday = today + dt.timedelta(days=days_to_sunday)
        last_sunday = current_sunday - dt.timedelta(days=7)
        time_key = last_sunday.strftime("%Y-w%V")

        logger.info(f"[管理排行榜] 时间键: {time_key}")

        conn = create_connection()

        try:
            # 删除上周排行榜数据
            delete_queries = [
                ("DELETE FROM talkplatform_game.user_rank_round WHERE time_key = %s", "time_key"),
                ("DELETE FROM talkplatform_game.rank_round WHERE time_key = %s", "time_key"),
                ("DELETE FROM talkplatform_game.rank_round_reward WHERE time_key = %s", "time_key")
            ]

            execute_batch_op(conn, delete_queries, time_key)

            # 重置机器人和用户状态
            update_queries = [
                ("UPDATE talkplatform_game.robot_rank SET use_status=0", "none"),
                ("UPDATE `talkplatform_game`.`user_rank_level` SET `use_flag` = 0, `del_flag` = 0", "none")
            ]

            execute_batch_op(conn, update_queries, "none")

            logger.info(f"[管理排行榜] 成功删除时间键 {time_key} 的数据并重置状态")

            return jsonify({
                'code': '0',
                'msg': '排行榜管理成功',
                'data': {
                    'time_key': time_key,
                    'operations': [
                        '删除上周排行榜数据',
                        '重置机器人使用状态',
                        '重置用户等级使用标志'
                    ]
                }
            })

        finally:
            conn.close()

    except Exception as e:
        logger.error(f"[管理排行榜] 错误: {e}")
        return jsonify({
            'code': '500',
            'msg': f'管理失败: {str(e)}',
            'data': None
        }), 500

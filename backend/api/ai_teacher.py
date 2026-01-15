# 文件: api/ai_teacher.py
# 作者: Claude Code
# 创建日期: 2026/01/14
# 描述: AI外教管理工具API

from flask import Blueprint, request, jsonify
import sys
import os
import logging
from datetime import datetime, timedelta
import requests

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 添加项目根目录以导入common模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from common.db_connect import create_connection

ai_teacher_bp = Blueprint('ai_teacher', __name__)

# 清空学习计划需要删除的表列表
CLEAR_PLAN_TABLES = [
    ("DELETE FROM `talkplatform_ai_teacher`.`user_info` WHERE user_info.id=%s", "id"),
    ("DELETE FROM `talkplatform_ai_teacher`.`user_lesson_consume_record` WHERE user_lesson_consume_record.user_id=%s", "id"),
    ("DELETE FROM `talkplatform_ai_teacher`.`user_lesson_exam_info` WHERE user_lesson_exam_info.user_id=%s", "id"),
    ("DELETE FROM `talkplatform_ai_teacher`.`user_report` WHERE user_report.user_id=%s", "user_id"),
    ("DELETE FROM `talkplatform_ai_teacher`.`user_test_analysis` WHERE user_test_analysis.user_id=%s", "user_id"),
    ("DELETE FROM `talkplatform_ai_teacher`.`user_statistics_gold_coin_log` WHERE user_statistics_gold_coin_log.user_id=%s", "user_id"),
    ("DELETE FROM `talkplatform_ai_teacher`.`user_week_statistics` WHERE user_week_statistics.user_id=%s", "user_id"),
    ("DELETE FROM `talkplatform_ai_teacher`.`user_week_plan` WHERE user_week_plan.user_id=%s", "user_id"),
    ("DELETE FROM `talkplatform_ai_teacher`.`user_timetable_finish_record` WHERE user_timetable_finish_record.user_id=%s", "user_id"),
    ("DELETE FROM `talkplatform_ai_teacher`.`user_statistics` WHERE user_statistics.user_id=%s", "user_id"),
    ("DELETE FROM `talkplatform_ai_teacher`.`user_timetable` WHERE user_timetable.user_id=%s", "user_id"),
    ("DELETE FROM `talkplatform_ai_teacher`.`user_update_log` WHERE user_update_log.user_id=%s", "user_id")
]


@ai_teacher_bp.route('/add_point', methods=['POST'])
def add_point():
    """
    为用户添加AI点数
    参数:
        user_id: 用户ID (必填)
        count: 点数数量 (可选，默认100)
        days: 有效天数 (可选，默认300)
    """
    try:
        data = request.json
        user_id = data.get('user_id')
        count = data.get('count', 100.00)
        days = data.get('days', 300)

        if not user_id:
            return jsonify({
                'code': '400',
                'msg': '用户ID不能为空',
                'data': None
            }), 400

        # 计算有效期
        start_date = datetime.now().strftime('%Y-%m-%d')
        end_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')

        logger.info(f"[AI点数添加] 用户ID: {user_id}, 点数: {count}, 有效期: {days}天")

        conn = create_connection()
        cursor = conn.cursor()

        try:
            # 插入AI点数
            add_query = """
                INSERT INTO `point`.`user_assets`
                (`stu_id`, `count`, `sku_id`, `sku_type`, `valid_start`, `valid_end`, `days`)
                VALUES (%s, %s, 113, 'ai_teach', %s, %s, %s)
            """
            cursor.execute(add_query, (user_id, count, start_date, end_date, days))
            conn.commit()

            logger.info(f"[AI点数添加] 成功添加 {count} 点到用户 {user_id}")

            return jsonify({
                'code': '0',
                'msg': f'成功添加 {count} AI点数',
                'data': {
                    'user_id': user_id,
                    'count': count,
                    'valid_start': start_date,
                    'valid_end': end_date,
                    'days': days
                }
            })

        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        logger.error(f"[AI点数添加] 错误: {e}")
        return jsonify({
            'code': '500',
            'msg': f'添加失败: {str(e)}',
            'data': None
        }), 500

@ai_teacher_bp.route('/query_point', methods=['POST'])
def query_point():
    """
    查询用户AI点数
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

        logger.info(f"[AI点数查询] 用户ID: {user_id}")

        conn = create_connection()
        cursor = conn.cursor()

        try:
            # 查询AI点数 - 只查询存在的字段
            query = """
                SELECT id, stu_id, count, valid_start, valid_end, days
                FROM `point`.`user_assets`
                WHERE stu_id = %s AND sku_type = 'ai_teach'
                ORDER BY id DESC
            """
            cursor.execute(query, (user_id,))
            results = cursor.fetchall()

            assets = []
            total_count = 0
            for row in results:
                asset = {
                    'id': row[0],
                    'user_id': row[1],
                    'count': float(row[2]),
                    'valid_start': str(row[3]),
                    'valid_end': str(row[4]),
                    'days': row[5]
                }
                assets.append(asset)
                total_count += float(row[2])

            logger.info(f"[AI点数查询] 用户 {user_id} 共有 {len(assets)} 条记录，总计 {total_count} 点")

            return jsonify({
                'code': '0',
                'msg': '查询成功',
                'data': {
                    'user_id': user_id,
                    'total_count': total_count,
                    'assets': assets
                }
            })

        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        logger.error(f"[AI点数查询] 错误: {e}")
        return jsonify({
            'code': '500',
            'msg': f'查询失败: {str(e)}',
            'data': None
        }), 500

@ai_teacher_bp.route('/use_exchange_code', methods=['POST'])
def use_exchange_code():
    """
    使用兑换码为用户兑换权益
    参数:
        user_id: 用户ID (必填)
        exchange_code: 兑换码 (必填)
    """
    try:
        data = request.json
        user_id = data.get('user_id')
        exchange_code = data.get('exchange_code')

        if not user_id:
            return jsonify({
                'code': '400',
                'msg': '用户ID不能为空',
                'data': None
            }), 400

        if not exchange_code:
            return jsonify({
                'code': '400',
                'msg': '兑换码不能为空',
                'data': None
            }), 400

        logger.info(f"[兑换码使用] 用户ID: {user_id}, 兑换码: {exchange_code}")

        # 调用第三方API
        api_url = f'http://172.16.16.36/talkplatform_leads_consumer/leads/third/tiktok/v1/front/user_exchange_order?order_exchange_code={exchange_code}&user_id={user_id}'

        response = requests.post(
            api_url,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )

        # 检查响应状态
        if response.status_code == 200:
            try:
                result = response.json()
                logger.info(f"[兑换码使用] 成功，响应: {result}")

                return jsonify({
                    'code': '0',
                    'msg': '兑换成功',
                    'data': {
                        'user_id': user_id,
                        'exchange_code': exchange_code,
                        'result': result
                    }
                })
            except Exception as e:
                logger.error(f"[兑换码使用] 解析响应失败: {e}")
                return jsonify({
                    'code': '0',
                    'msg': '兑换请求已发送',
                    'data': {
                        'user_id': user_id,
                        'exchange_code': exchange_code,
                        'response_text': response.text
                    }
                })
        else:
            logger.error(f"[兑换码使用] 失败，状态码: {response.status_code}, 响应: {response.text}")
            return jsonify({
                'code': '500',
                'msg': f'兑换失败，状态码: {response.status_code}',
                'data': {
                    'status_code': response.status_code,
                    'response_text': response.text
                }
            }), 500

    except requests.exceptions.Timeout:
        logger.error(f"[兑换码使用] 请求超时")
        return jsonify({
            'code': '500',
            'msg': '兑换请求超时，请稍后重试',
            'data': None
        }), 500
    except Exception as e:
        logger.error(f"[兑换码使用] 错误: {e}")
        return jsonify({
            'code': '500',
            'msg': f'兑换失败: {str(e)}',
            'data': None
        }), 500

@ai_teacher_bp.route('/clear_study_plan', methods=['POST'])
def clear_study_plan():
    """
    清空用户所有学习计划数据
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

        logger.info(f"[清空学习计划] 用户ID: {user_id}")

        conn = create_connection()
        cursor = conn.cursor()

        deleted_tables = []
        failed_tables = []

        try:
            # 开始事务
            conn.begin()

            # 逐个表删除数据
            for sql, _ in CLEAR_PLAN_TABLES:
                table_name = sql.split('`')[3]  # 提取表名
                try:
                    cursor.execute(sql, (user_id,))
                    affected_rows = cursor.rowcount
                    deleted_tables.append({
                        'table': table_name,
                        'deleted_count': affected_rows
                    })
                    logger.info(f"[清空学习计划] 表 {table_name} 删除 {affected_rows} 条记录")
                except Exception as e:
                    failed_tables.append({
                        'table': table_name,
                        'error': str(e)
                    })
                    logger.error(f"[清空学习计划] 表 {table_name} 删除失败: {e}")

            # 提交事务
            conn.commit()

            total_deleted = sum(item['deleted_count'] for item in deleted_tables)

            logger.info(f"[清空学习计划] 用户 {user_id} 清空完成，共删除 {total_deleted} 条记录")

            return jsonify({
                'code': '0',
                'msg': f'成功清空学习计划，共删除 {total_deleted} 条记录',
                'data': {
                    'user_id': user_id,
                    'total_deleted': total_deleted,
                    'deleted_tables': deleted_tables,
                    'failed_tables': failed_tables,
                    'success_count': len(deleted_tables),
                    'failed_count': len(failed_tables)
                }
            })

        except Exception as e:
            # 回滚事务
            conn.rollback()
            logger.error(f"[清空学习计划] 事务回滚: {e}")
            return jsonify({
                'code': '500',
                'msg': f'清空失败，事务已回滚: {str(e)}',
                'data': None
            }), 500

        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        logger.error(f"[清空学习计划] 错误: {e}")
        return jsonify({
            'code': '500',
            'msg': f'清空失败: {str(e)}',
            'data': None
        }), 500

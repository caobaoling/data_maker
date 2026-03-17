# 文件: api/user.py
# 作者: Claude Code
# 创建日期: 2026/03/12
# 描述: 用户管理工具API

from flask import Blueprint, request, jsonify
import sys
import os
import logging
from datetime import datetime, timedelta

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 添加项目根目录以导入common模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from common.db_connect import create_connection

user_bp = Blueprint('user', __name__)

# 财富类型配置
WEALTH_TYPES = {
    'point': {'sku_id': 1, 'name': '次卡'},
    'classtime': {'sku_id': 19, 'name': '课时'},
    'pthpoint': {'sku_id': 104, 'name': '普通话'},
    'ar_point': {'sku_id': 109, 'name': '阿教次卡'},
    'ai_podcast': {'sku_id': 117, 'name': 'AI播客'},
    'academy': {'sku_id': 116, 'name': '中东学院'},
    'ai_teach': {'sku_id': 113, 'name': 'AI外教'},
    'pbook': {'sku_id': 106, 'name': '51绘本'},
    'word1v1': {'sku_id': 111, 'name': '正课课时'},
    'word_review1v1': {'sku_id': 112, 'name': '抗遗忘课时'},
    'jp_point': {'sku_id': 108, 'name': '日本本地课时'}
}

@user_bp.route('/add_wealth', methods=['POST'])
def add_wealth():
    """
    为用户添加财富
    参数:
        user_id: 用户ID (必填)
        sku_type: 财富类型 (必填)
        count: 数量 (可选，默认100)
        days: 有效天数 (可选，默认300)
    """
    try:
        data = request.json
        user_id = data.get('user_id')
        sku_type = data.get('sku_type')
        count = data.get('count', 100.00)
        days = data.get('days', 300)

        if not user_id:
            return jsonify({
                'code': '400',
                'msg': '用户ID不能为空',
                'data': None
            }), 400

        if not sku_type:
            return jsonify({
                'code': '400',
                'msg': '财富类型不能为空',
                'data': None
            }), 400

        if sku_type not in WEALTH_TYPES:
            return jsonify({
                'code': '400',
                'msg': f'不支持的财富类型: {sku_type}',
                'data': None
            }), 400

        wealth_config = WEALTH_TYPES[sku_type]
        sku_id = wealth_config['sku_id']
        wealth_name = wealth_config['name']

        # 计算有效期
        start_date = datetime.now().strftime('%Y-%m-%d')
        end_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')

        logger.info(f"[添加财富] 用户ID: {user_id}, 类型: {wealth_name}({sku_type}), 数量: {count}, 有效期: {days}天")

        conn = create_connection()
        cursor = conn.cursor()

        try:
            # 插入财富记录
            add_query = """
                INSERT INTO `point`.`user_assets`
                (`stu_id`, `count`, `sku_id`, `sku_type`, `valid_start`, `valid_end`, `days`)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(add_query, (user_id, count, sku_id, sku_type, start_date, end_date, days))
            conn.commit()

            logger.info(f"[添加财富] 成功添加 {count} {wealth_name} 到用户 {user_id}")

            return jsonify({
                'code': '0',
                'msg': f'成功添加 {count} {wealth_name}',
                'data': {
                    'user_id': user_id,
                    'sku_type': sku_type,
                    'sku_id': sku_id,
                    'wealth_name': wealth_name,
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
        logger.error(f"[添加财富] 错误: {e}")
        return jsonify({
            'code': '500',
            'msg': f'添加失败: {str(e)}',
            'data': None
        }), 500

@user_bp.route('/query_wealth', methods=['POST'])
def query_wealth():
    """
    查询用户财富
    参数:
        user_id: 用户ID (必填)
        sku_type: 财富类型 (可选，不传则查询所有类型)
    """
    try:
        data = request.json
        user_id = data.get('user_id')
        sku_type = data.get('sku_type')

        if not user_id:
            return jsonify({
                'code': '400',
                'msg': '用户ID不能为空',
                'data': None
            }), 400

        logger.info(f"[查询财富] 用户ID: {user_id}, 类型: {sku_type or '全部'}")

        conn = create_connection()
        cursor = conn.cursor()

        try:
            # 构建查询SQL
            if sku_type:
                if sku_type not in WEALTH_TYPES:
                    return jsonify({
                        'code': '400',
                        'msg': f'不支持的财富类型: {sku_type}',
                        'data': None
                    }), 400

                query = """
                    SELECT id, stu_id, count, sku_id, sku_type, valid_start, valid_end, days, status
                    FROM `point`.`user_assets`
                    WHERE stu_id = %s AND sku_type = %s
                    ORDER BY id DESC
                """
                cursor.execute(query, (user_id, sku_type))
            else:
                query = """
                    SELECT id, stu_id, count, sku_id, sku_type, valid_start, valid_end, days, status
                    FROM `point`.`user_assets`
                    WHERE stu_id = %s
                    ORDER BY sku_type, id DESC
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
                    'sku_id': row[3],
                    'sku_type': row[4],
                    'wealth_name': WEALTH_TYPES.get(row[4], {}).get('name', '未知类型'),
                    'valid_start': str(row[5]),
                    'valid_end': str(row[6]),
                    'days': row[7],
                    'status': row[8]
                }
                assets.append(asset)
                total_count += float(row[2])

            logger.info(f"[查询财富] 用户 {user_id} 共有 {len(assets)} 条记录，总计 {total_count}")

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
        logger.error(f"[查询财富] 错误: {e}")
        return jsonify({
            'code': '500',
            'msg': f'查询失败: {str(e)}',
            'data': None
        }), 500

@user_bp.route('/wealth_types', methods=['GET'])
def get_wealth_types():
    """
    获取所有支持的财富类型
    """
    try:
        types_list = [
            {
                'sku_type': key,
                'sku_id': value['sku_id'],
                'name': value['name']
            }
            for key, value in WEALTH_TYPES.items()
        ]

        return jsonify({
            'code': '0',
            'msg': '获取成功',
            'data': types_list
        })
    except Exception as e:
        logger.error(f"[获取财富类型] 错误: {e}")
        return jsonify({
            'code': '500',
            'msg': f'获取失败: {str(e)}',
            'data': None
        }), 500


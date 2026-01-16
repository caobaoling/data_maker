# 文件: api/picturebook.py
# 作者: Claude Code
# 创建日期: 2026/01/16
# 描述: 绘本系统相关API - 清除学习计划

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

from common.db_connect import create_connection
from common.delete_redis import RedisKeyDeleter

picturebook_bp = Blueprint('picturebook', __name__)

@picturebook_bp.route('/clear_plan', methods=['POST'])
def clear_picturebook_plan():
    """
    清除用户绘本学习计划
    包括两步:
    1. 删除数据库中的12个表的数据
    2. 清除Redis缓存 (使用模糊匹配删除用户相关键)
    """
    try:
        data = request.json
        user_id = data.get('user_id')

        if not user_id:
            return jsonify({
                'code': '40000',
                'message': '用户ID不能为空',
                'data': None
            }), 400

        logger.info(f"[绘本清理] 开始清理用户 {user_id} 的绘本数据")

        # ========== 第一步: 删除数据库数据 ==========

        # 计算分表后缀 (用户ID后两位, 如 03 取 3, 13 取 13)
        suffix = int(str(user_id)[-2:])
        logger.info(f"[绘本清理] 用户ID后两位: {suffix}")

        # 构建SQL语句列表 (按照原始SQL顺序)
        delete_queries = [
            f"DELETE FROM talkplatform_ai_pbook.user_info WHERE id = {user_id}",
            f"DELETE FROM talkplatform_ai_pbook.user_settlement_{suffix} WHERE stu_id = {user_id}",
            f"DELETE FROM talkplatform_ai_pbook.user_weekly_statistics WHERE stu_id = {user_id}",
            f"DELETE FROM talkplatform_ai_pbook.course_package_reading_plan WHERE stu_id = {user_id}",
            f"DELETE FROM talkplatform_ai_pbook.weekly_report WHERE stu_id = {user_id}",
            f"DELETE FROM talkplatform_ai_pbook.user_report_{suffix} WHERE stu_id = {user_id}",
            f"DELETE FROM talkplatform_ai_pbook.user_practice_{suffix} WHERE stu_id = {user_id}",
            f"DELETE FROM talkplatform_ai_pbook.user_game_asset_record_{suffix} WHERE stu_id = {user_id}",
            f"DELETE FROM talkplatform_ai_pbook.user_daily_statistics_info WHERE stu_id = {user_id}",
            f"DELETE FROM talkplatform_ai_pbook.picture_book_reading_plan_{suffix} WHERE stu_id = {user_id}",
            f"DELETE FROM talkplatform_ai_pbook.reading_setting WHERE stu_id = {user_id}"
        ]

        # 连接数据库
        conn = create_connection()
        if not conn:
            return jsonify({
                'code': '50000',
                'message': '数据库连接失败',
                'data': None
            }), 500

        try:
            cursor = conn.cursor()
            deleted_counts = {}

            # 执行每条删除语句
            for i, sql in enumerate(delete_queries, 1):
                try:
                    # 提取表名用于日志
                    table_name = sql.split('FROM')[1].split('WHERE')[0].strip()

                    logger.info(f"[绘本清理] 执行SQL {i}/{len(delete_queries)}: {sql[:60]}...")
                    cursor.execute(sql)
                    rows_affected = cursor.rowcount
                    deleted_counts[table_name] = rows_affected
                    logger.info(f"[绘本清理] 表 {table_name} 删除了 {rows_affected} 条记录")

                except Exception as e:
                    logger.warning(f"[绘本清理] SQL执行警告 (可能表不存在): {str(e)[:100]}")
                    # 继续执行下一条,不中断整个流程
                    continue

            # 提交事务
            conn.commit()
            cursor.close()
            conn.close()

            total_deleted = sum(deleted_counts.values())
            logger.info(f"[绘本清理] 数据库清理完成,共删除 {total_deleted} 条记录")

        except Exception as e:
            logger.error(f"[绘本清理] 数据库操作异常: {str(e)}", exc_info=True)
            if conn:
                conn.rollback()
                conn.close()
            return jsonify({
                'code': '50000',
                'message': f'数据库操作失败: {str(e)}',
                'data': None
            }), 500

        # ========== 第二步: 清除Redis缓存 ==========

        logger.info(f"[绘本清理] 开始清理用户 {user_id} 的Redis缓存")

        # 绘本系统使用两个Redis节点
        redis_nodes = [
            {'host': '172.16.70.21', 'port': 6381, 'password': None},
            {'host': '172.16.70.21', 'port': 6382, 'password': None}
        ]

        # 构建用户相关的Redis键模式
        # 常见模式: user:*:用户ID*, *:用户ID, 用户ID:*
        patterns = [
            f"*{user_id}*",         # 包含用户ID的所有键
            f"user:{user_id}:*",    # user:用户ID: 开头的键
            f"*:user:{user_id}*",   # 包含 :user:用户ID 的键
        ]

        redis_deleted_total = 0
        redis_deleted_keys = []
        redis_nodes_result = {}

        try:
            # 遍历每个Redis节点
            for node_index, node in enumerate(redis_nodes, 1):
                node_name = f"{node['host']}:{node['port']}"
                logger.info(f"[绘本清理] 正在清理Redis节点 {node_index}/2: {node_name}")

                try:
                    deleter = RedisKeyDeleter(node['host'], node['port'], node['password'])
                    node_deleted_count = 0
                    node_deleted_keys = []

                    # 对当前节点执行所有模式的删除
                    for pattern in patterns:
                        try:
                            count, keys = deleter.delete_keys_by_pattern(
                                pattern,
                                batch_size=100,
                                dry_run=False,  # 直接删除,不预览
                                confirm=False   # 不需要用户确认
                            )
                            node_deleted_count += count
                            node_deleted_keys.extend(keys)
                            if count > 0:
                                logger.info(f"[绘本清理] 节点{node_name} 模式'{pattern}' 删除了 {count} 个键")
                        except Exception as e:
                            logger.warning(f"[绘本清理] 节点{node_name} 模式'{pattern}' 删除失败: {str(e)}")
                            continue

                    deleter.close()

                    redis_deleted_total += node_deleted_count
                    redis_deleted_keys.extend(node_deleted_keys[:5])  # 每个节点取前5个键作为示例
                    redis_nodes_result[node_name] = node_deleted_count

                    logger.info(f"[绘本清理] 节点{node_name} 清理完成,共删除 {node_deleted_count} 个键")

                except Exception as e:
                    logger.error(f"[绘本清理] 节点{node_name} 连接失败: {str(e)}")
                    redis_nodes_result[node_name] = 0
                    continue

            logger.info(f"[绘本清理] Redis清理完成,共删除 {redis_deleted_total} 个键 (节点详情: {redis_nodes_result})")

        except Exception as e:
            logger.error(f"[绘本清理] Redis清理异常: {str(e)}", exc_info=True)
            # Redis清理失败不影响整体返回成功 (数据库已清理)
            redis_deleted_total = 0
            redis_nodes_result = {}

        # ========== 返回结果 ==========

        return jsonify({
            'code': '10000',
            'message': '绘本学习计划清除成功',
            'data': {
                'user_id': user_id,
                'database': {
                    'total_deleted': total_deleted,
                    'details': deleted_counts
                },
                'redis': {
                    'total_deleted': redis_deleted_total,
                    'nodes_result': redis_nodes_result,  # 新增: 每个节点的删除统计
                    'sample_keys': redis_deleted_keys[:10] if redis_deleted_keys else []
                }
            }
        })

    except Exception as e:
        logger.error(f"[绘本清理] 异常: {str(e)}", exc_info=True)
        return jsonify({
            'code': '50000',
            'message': f'请求失败: {str(e)}',
            'data': None
        }), 500

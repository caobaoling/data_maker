# 文件: api/redis.py
# 作者: Claude Code
# 创建日期: 2026/01/13
# 描述: Redis管理工具API

from flask import Blueprint, request, jsonify
import sys
import os
import logging
import redis
from typing import List, Dict, Any

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 添加项目根目录以导入common模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from common.delete_redis import RedisKeyDeleter

redis_bp = Blueprint('redis', __name__)

# Redis连接配置（默认配置，可通过请求参数覆盖）
DEFAULT_REDIS_CONFIG = {
    'host': '172.16.70.21',
    'port': 6379,
    'password': None
}

# 预定义的Redis节点列表
REDIS_NODES = [
    {'host': '172.16.70.21', 'port': 6379, 'name': 'Redis-6379'},
    {'host': '172.16.70.21', 'port': 6382, 'name': 'Redis-6382'},
    {'host': '172.16.70.21', 'port': 6381, 'name': 'Redis-6381'}
]

def get_redis_connection(config: Dict[str, Any] = None) -> redis.Redis:
    """创建Redis连接"""
    if config is None:
        config = DEFAULT_REDIS_CONFIG

    try:
        r = redis.Redis(
            host=config.get('host', DEFAULT_REDIS_CONFIG['host']),
            port=int(config.get('port', DEFAULT_REDIS_CONFIG['port'])),
            password=config.get('password', DEFAULT_REDIS_CONFIG['password']),
            socket_timeout=10
        )
        # 测试连接
        r.ping()
        return r
    except Exception as e:
        logger.error(f"Redis连接失败: {e}")
        raise

@redis_bp.route('/config', methods=['GET'])
def get_config():
    """获取默认Redis配置"""
    return jsonify({
        'code': '0',
        'msg': '获取成功',
        'data': {
            'default': DEFAULT_REDIS_CONFIG,
            'nodes': REDIS_NODES
        }
    })

@redis_bp.route('/search', methods=['POST'])
def search_keys():
    """
    搜索Redis键
    参数:
        pattern: 搜索模式 (如: user:*, *cache*)
        redis_config: Redis连接配置 (可选)
    """
    try:
        data = request.json
        pattern = data.get('pattern', '*')
        redis_config = data.get('redis_config', DEFAULT_REDIS_CONFIG)

        logger.info(f"[Redis搜索] 模式: {pattern}")

        r = get_redis_connection(redis_config)

        # 使用SCAN命令搜索键
        matched_keys = []
        cursor = 0
        scan_count = 0

        while True:
            cursor, keys = r.scan(cursor=cursor, match=pattern, count=1000)
            scan_count += 1

            if keys:
                # 解码键名
                decoded_keys = [
                    key.decode('utf-8') if isinstance(key, bytes) else str(key)
                    for key in keys
                ]
                matched_keys.extend(decoded_keys)

            if cursor == 0:
                break

        logger.info(f"[Redis搜索] 找到 {len(matched_keys)} 个匹配的键")

        return jsonify({
            'code': '0',
            'msg': '搜索成功',
            'data': {
                'keys': matched_keys,
                'count': len(matched_keys)
            }
        })

    except Exception as e:
        logger.error(f"[Redis搜索] 错误: {e}")
        return jsonify({
            'code': '500',
            'msg': f'搜索失败: {str(e)}',
            'data': None
        }), 500

@redis_bp.route('/key/info', methods=['POST'])
def get_key_info():
    """
    获取键的详细信息
    参数:
        key: 键名
        redis_config: Redis连接配置 (可选)
    """
    try:
        data = request.json
        key = data.get('key')
        redis_config = data.get('redis_config', DEFAULT_REDIS_CONFIG)

        if not key:
            return jsonify({
                'code': '400',
                'msg': '键名不能为空',
                'data': None
            }), 400

        r = get_redis_connection(redis_config)

        # 检查键是否存在
        if not r.exists(key):
            return jsonify({
                'code': '404',
                'msg': '键不存在',
                'data': None
            }), 404

        # 获取键的类型
        key_type = r.type(key).decode('utf-8') if isinstance(r.type(key), bytes) else str(r.type(key))

        # 获取TTL
        ttl = r.ttl(key)

        # 根据类型获取值
        value = None
        value_str = None

        try:
            if key_type == 'string':
                raw_value = r.get(key)
                if isinstance(raw_value, bytes):
                    value_str = raw_value.decode('utf-8')
                else:
                    value_str = str(raw_value)
                value = value_str

            elif key_type == 'hash':
                raw_hash = r.hgetall(key)
                value = {
                    k.decode('utf-8') if isinstance(k, bytes) else str(k):
                    v.decode('utf-8') if isinstance(v, bytes) else str(v)
                    for k, v in raw_hash.items()
                }
                value_str = str(value)

            elif key_type == 'list':
                raw_list = r.lrange(key, 0, 100)  # 限制前100个元素
                value = [
                    item.decode('utf-8') if isinstance(item, bytes) else str(item)
                    for item in raw_list
                ]
                list_len = r.llen(key)
                value_str = f"List(长度: {list_len})"

            elif key_type == 'set':
                raw_set = r.smembers(key)
                value = [
                    item.decode('utf-8') if isinstance(item, bytes) else str(item)
                    for item in raw_set
                ]
                value_str = f"Set(成员数: {len(value)})"

            elif key_type == 'zset':
                raw_zset = r.zrange(key, 0, 100, withscores=True)  # 限制前100个元素
                value = [
                    {
                        'member': member.decode('utf-8') if isinstance(member, bytes) else str(member),
                        'score': score
                    }
                    for member, score in raw_zset
                ]
                zset_len = r.zcard(key)
                value_str = f"ZSet(成员数: {zset_len})"

            else:
                value_str = f"不支持的类型: {key_type}"

        except Exception as e:
            value_str = f"读取值失败: {str(e)}"

        return jsonify({
            'code': '0',
            'msg': '获取成功',
            'data': {
                'key': key,
                'type': key_type,
                'ttl': ttl,
                'value': value,
                'value_str': value_str
            }
        })

    except Exception as e:
        logger.error(f"[Redis键信息] 错误: {e}")
        return jsonify({
            'code': '500',
            'msg': f'获取键信息失败: {str(e)}',
            'data': None
        }), 500

@redis_bp.route('/key/delete', methods=['POST'])
def delete_keys():
    """
    删除Redis键
    参数:
        keys: 键列表 (数组)
        redis_config: Redis连接配置 (可选)
    """
    try:
        data = request.json
        keys = data.get('keys', [])
        redis_config = data.get('redis_config', DEFAULT_REDIS_CONFIG)

        if not keys:
            return jsonify({
                'code': '400',
                'msg': '键列表不能为空',
                'data': None
            }), 400

        logger.info(f"[Redis删除] 准备删除 {len(keys)} 个键")

        r = get_redis_connection(redis_config)

        # 批量删除
        deleted_count = 0
        failed_keys = []

        for key in keys:
            try:
                if r.delete(key):
                    deleted_count += 1
            except Exception as e:
                logger.error(f"[Redis删除] 删除键 {key} 失败: {e}")
                failed_keys.append(key)

        logger.info(f"[Redis删除] 成功删除 {deleted_count} 个键")

        return jsonify({
            'code': '0',
            'msg': f'成功删除 {deleted_count} 个键',
            'data': {
                'deleted_count': deleted_count,
                'failed_keys': failed_keys
            }
        })

    except Exception as e:
        logger.error(f"[Redis删除] 错误: {e}")
        return jsonify({
            'code': '500',
            'msg': f'删除失败: {str(e)}',
            'data': None
        }), 500

@redis_bp.route('/key/delete_by_pattern', methods=['POST'])
def delete_by_pattern():
    """
    按模式批量删除Redis键
    参数:
        pattern: 匹配模式 (如: user:*, *cache*)
        redis_config: Redis连接配置 (可选)
        dry_run: 是否为预览模式（默认True，只查询不删除）
    """
    try:
        data = request.json
        pattern = data.get('pattern')
        redis_config = data.get('redis_config', DEFAULT_REDIS_CONFIG)
        dry_run = data.get('dry_run', True)  # 默认为预览模式

        if not pattern:
            return jsonify({
                'code': '400',
                'msg': '匹配模式不能为空',
                'data': None
            }), 400

        mode_text = "预览" if dry_run else "删除"
        logger.info(f"[Redis模式{mode_text}] 模式: {pattern}, dry_run: {dry_run}")

        # 使用RedisKeyDeleter类进行操作
        deleter = RedisKeyDeleter(
            redis_host=redis_config.get('host', DEFAULT_REDIS_CONFIG['host']),
            redis_port=int(redis_config.get('port', DEFAULT_REDIS_CONFIG['port'])),
            redis_password=redis_config.get('password', DEFAULT_REDIS_CONFIG['password'])
        )

        try:
            # 执行操作（dry_run=True时只查询，False时实际删除）
            deleted_count, deleted_keys = deleter.delete_keys_by_pattern(
                pattern=pattern,
                batch_size=1000,
                dry_run=dry_run,
                confirm=False  # 由前端确认
            )

            if dry_run:
                logger.info(f"[Redis预览] 找到 {deleted_count} 个匹配的键")
                return jsonify({
                    'code': '0',
                    'msg': f'找到 {deleted_count} 个匹配的键',
                    'data': {
                        'count': deleted_count,
                        'keys': deleted_keys[:100],  # 返回前100个键名供预览
                        'preview_count': min(100, len(deleted_keys)),
                        'has_more': len(deleted_keys) > 100
                    }
                })
            else:
                logger.info(f"[Redis删除] 成功删除 {deleted_count} 个键")
                return jsonify({
                    'code': '0',
                    'msg': f'成功删除 {deleted_count} 个键',
                    'data': {
                        'deleted_count': deleted_count,
                        'deleted_keys': deleted_keys[:100]  # 只返回前100个键名
                    }
                })

        finally:
            deleter.close()

    except Exception as e:
        logger.error(f"[Redis操作] 错误: {e}")
        return jsonify({
            'code': '500',
            'msg': f'操作失败: {str(e)}',
            'data': None
        }), 500

@redis_bp.route('/stats', methods=['POST'])
def get_stats():
    """
    获取Redis统计信息
    参数:
        redis_config: Redis连接配置 (可选)
    """
    try:
        data = request.json or {}
        redis_config = data.get('redis_config', DEFAULT_REDIS_CONFIG)

        r = get_redis_connection(redis_config)

        # 获取数据库大小
        db_size = r.dbsize()

        # 获取info信息
        info = r.info()

        stats = {
            'db_size': db_size,
            'used_memory': info.get('used_memory_human', 'N/A'),
            'connected_clients': info.get('connected_clients', 0),
            'total_commands_processed': info.get('total_commands_processed', 0),
            'redis_version': info.get('redis_version', 'N/A'),
            'uptime_in_days': info.get('uptime_in_days', 0)
        }

        return jsonify({
            'code': '0',
            'msg': '获取成功',
            'data': stats
        })

    except Exception as e:
        logger.error(f"[Redis统计] 错误: {e}")
        return jsonify({
            'code': '500',
            'msg': f'获取统计信息失败: {str(e)}',
            'data': None
        }), 500

@redis_bp.route('/ping', methods=['POST'])
def ping():
    """
    测试Redis连接
    参数:
        redis_config: Redis连接配置
    """
    try:
        data = request.json
        redis_config = data.get('redis_config', DEFAULT_REDIS_CONFIG)

        r = get_redis_connection(redis_config)
        r.ping()

        return jsonify({
            'code': '0',
            'msg': 'Redis连接正常',
            'data': {
                'host': redis_config.get('host'),
                'port': redis_config.get('port')
            }
        })

    except Exception as e:
        logger.error(f"[Redis连接测试] 错误: {e}")
        return jsonify({
            'code': '500',
            'msg': f'连接失败: {str(e)}',
            'data': None
        }), 500

@redis_bp.route('/multi_node/delete_by_pattern', methods=['POST'])
def multi_node_delete_by_pattern():
    """
    多节点按模式批量删除Redis键（参考 delete_redis.py 的 multi_server_delete）
    参数:
        pattern: 匹配模式 (如: user:*, *cache*)
        nodes: Redis节点列表 [{'host': '...', 'port': ...}, ...]
        dry_run: 是否为预览模式（默认True）
    """
    try:
        data = request.json
        pattern = data.get('pattern')
        nodes = data.get('nodes', REDIS_NODES)  # 默认使用所有预定义节点
        dry_run = data.get('dry_run', True)
        password = data.get('password', None)

        if not pattern:
            return jsonify({
                'code': '400',
                'msg': '匹配模式不能为空',
                'data': None
            }), 400

        if not nodes:
            return jsonify({
                'code': '400',
                'msg': '节点列表不能为空',
                'data': None
            }), 400

        mode_text = "预览" if dry_run else "删除"
        logger.info(f"[多节点{mode_text}] 模式: {pattern}, 节点数: {len(nodes)}, dry_run: {dry_run}")

        # 记录每个节点的结果
        node_results = []
        total_count = 0
        total_deleted = 0
        all_keys = []

        # 遍历所有节点
        for node in nodes:
            node_host = node.get('host')
            node_port = node.get('port')
            node_name = node.get('name', f"{node_host}:{node_port}")

            logger.info(f"[多节点{mode_text}] 正在处理节点 -> {node_name}")

            try:
                # 为每个节点创建RedisKeyDeleter
                deleter = RedisKeyDeleter(
                    redis_host=node_host,
                    redis_port=int(node_port),
                    redis_password=password
                )

                try:
                    # 执行操作
                    count, keys = deleter.delete_keys_by_pattern(
                        pattern=pattern,
                        batch_size=1000,
                        dry_run=dry_run,
                        confirm=False
                    )

                    node_results.append({
                        'node': node_name,
                        'host': node_host,
                        'port': node_port,
                        'success': True,
                        'count': count,
                        'keys': keys[:20] if dry_run else []  # 预览模式返回前20个键
                    })

                    total_count += count
                    if dry_run:
                        all_keys.extend(keys[:20])  # 每个节点收集前20个键
                    else:
                        total_deleted += count

                    logger.info(f"[多节点{mode_text}] 节点 {node_name} 处理完成，{'找到' if dry_run else '删除'} {count} 个键")

                finally:
                    deleter.close()

            except Exception as e:
                logger.error(f"[多节点{mode_text}] 处理节点 {node_name} 时出错: {e}")
                node_results.append({
                    'node': node_name,
                    'host': node_host,
                    'port': node_port,
                    'success': False,
                    'error': str(e),
                    'count': 0
                })
                continue  # 一个节点失败，继续处理下一个

        # 返回结果
        if dry_run:
            logger.info(f"[多节点预览] 完成！总共找到 {total_count} 个键")
            return jsonify({
                'code': '0',
                'msg': f'在 {len(nodes)} 个节点上找到 {total_count} 个匹配的键',
                'data': {
                    'total_count': total_count,
                    'node_results': node_results,
                    'preview_keys': all_keys[:100],  # 返回前100个键供预览
                    'has_more': total_count > 100
                }
            })
        else:
            logger.info(f"[多节点删除] 完成！总共删除 {total_deleted} 个键")
            return jsonify({
                'code': '0',
                'msg': f'成功在 {len(nodes)} 个节点上删除 {total_deleted} 个键',
                'data': {
                    'total_deleted': total_deleted,
                    'node_results': node_results
                }
            })

    except Exception as e:
        logger.error(f"[多节点操作] 错误: {e}")
        return jsonify({
            'code': '500',
            'msg': f'操作失败: {str(e)}',
            'data': None
        }), 500

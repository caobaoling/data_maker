# 文件: search_redis
# 作者: bao0
# 创建日期: 2025/9/29
# 描述: 这是一个搜索redis缓存的文件#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Redis搜索脚本
用于连接Redis服务器并模糊搜索指定模式的键
"""

import redis
import logging
import sys

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def search_redis_keys(redis_host, redis_port, redis_password, pattern, batch_size=1000):
    """
    搜索Redis中匹配指定模式的所有键

    Args:
        redis_host (str): Redis主机地址
        redis_port (int): Redis端口号
        redis_password (str): Redis密码
        pattern (str): 要匹配的键模式
        batch_size (int): 每次扫描的键数量

    Returns:
        list: 匹配的键列表
    """
    try:
        # 连接到Redis
        logging.info(f"尝试连接到Redis服务器 {redis_host}:{redis_port}")
        r = redis.Redis(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            socket_timeout=5,
            # decode_responses=True
        )

        # 测试连接
        r.ping()
        logging.info("成功连接到Redis服务器")

        matched_keys = []
        cursor = 0
        scan_count = 0

        logging.info(f"开始扫描匹配模式 '{pattern}' 的键")

        while True:
            cursor, keys = r.scan(cursor=cursor, match=pattern, count=batch_size)
            scan_count += 1

            if keys:
                # 手动解码字节类型键名
                decoded_keys = [key.decode('utf-8') if isinstance(key, bytes) else key for key in keys]

                matched_keys.extend(decoded_keys)
                logging.info(f"第{scan_count}次扫描，找到{len(keys)}个匹配的键")

            # 如果cursor为0，说明扫描完成
            if cursor == 0:
                break

        logging.info(f"扫描完成，总共找到 {len(matched_keys)} 个匹配的键")
        return matched_keys

    except redis.ConnectionError as e:
        logging.error(f"Redis连接错误: {e}")
        return []
    except redis.AuthenticationError as e:
        logging.error(f"Redis认证错误: {e}")
        return []
    except redis.RedisError as e:
        logging.error(f"Redis操作错误: {e}")
        return []
    except Exception as e:
        logging.error(f"未知错误: {e}")
        return []

def get_key_values(redis_host, redis_port, redis_password, keys):
    """
    获取指定键的值

    Args:
        redis_host (str): Redis主机地址
        redis_port (int): Redis端口号
        redis_password (str): Redis密码
        keys (list): 键列表

    Returns:
        dict: 键值对字典
    """
    try:
        r = redis.Redis(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            socket_timeout=5,
            # decode_responses=True
        )

        key_values = {}
        for key in keys:
            try:
                key_type = r.type(key)
                if key_type == 'string':
                    value = r.get(key)
                elif key_type == 'hash':
                    value = r.hgetall(key)
                elif key_type == 'list':
                    value = r.lrange(key, 0, -1)
                elif key_type == 'set':
                    value = r.smembers(key)
                elif key_type == 'zset':
                    value = r.zrange(key, 0, -1, withscores=True)
                else:
                    value = f"Unsupported type: {key_type}"

                key_values[key] = {
                    'type': key_type,
                    'value': value
                }
            except Exception as e:
                key_values[key] = {
                    'type': 'error',
                    'value': str(e)
                }

        return key_values
    except Exception as e:
        logging.error(f"获取键值时出错: {e}")
        return {}

def main():
    """主函数"""
    # Redis连接配置
    REDIS_HOST = '172.16.70.21'
    REDIS_PORT = 6379
    REDIS_PASSWORD = None

    # 搜索模式
    search_pattern = "appoint_multi_redis_appoint_info__1958813181"  # 模糊搜索包含"195881"的键

    print(f"Redis服务器: {REDIS_HOST}:{REDIS_PORT}")
    print(f"搜索模式: {search_pattern}")

    # 搜索匹配的键
    matched_keys = search_redis_keys(
        REDIS_HOST,
        REDIS_PORT,
        REDIS_PASSWORD,
        search_pattern
    )

    if not matched_keys:
        print("未找到匹配的键")
        return

    print(f"\n找到 {len(matched_keys)} 个匹配的键:")
    for i, key in enumerate(matched_keys[:20], 1):  # 只显示前20个
        print(f"{i:2d}. {key}")

    if len(matched_keys) > 20:
        print(f"... 还有 {len(matched_keys) - 20} 个键")

    # 询问是否查看键的值
    if len(matched_keys) <= 10:  # 如果键数量不多，直接显示
        show_values = 'y'
    else:
        show_values = input("\n是否显示这些键的值？(y/N): ")

    if show_values.lower() in ['y', 'yes']:
        print("\n获取键值...")
        key_values = get_key_values(
            REDIS_HOST,
            REDIS_PORT,
            REDIS_PASSWORD,
            matched_keys[:10]  # 限制获取前10个键的值
        )

        for key, data in key_values.items():
            print(f"\n键: {key}")
            print(f"类型: {data['type']}")
            print(f"值: {data['value']}")

if __name__ == "__main__":
    main()

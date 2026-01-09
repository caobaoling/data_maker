#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# 文件: delete_redis
# 作者: bao0
# 创建日期: 2025/1/15
# 修改日期: 2025/9/29
# 描述: Redis批量删除工具 - 支持多种删除方式
"""
try:
    unicode  # type: ignore
except NameError:
    unicode = str

import redis
import logging
import time
from typing import List, Optional, Tuple

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class RedisKeyDeleter:
    """Redis批量删除工具类"""
    
    def __init__(self, redis_host: str, redis_port: int, redis_password: Optional[str] = None, 
                 socket_timeout: int = 30):
        """
        初始化Redis连接
        
        Args:
            redis_host: Redis主机地址
            redis_port: Redis端口号
            redis_password: Redis密码
            socket_timeout: 连接超时时间（秒）
        """
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_password = redis_password
        self.socket_timeout = socket_timeout
        self._connection = None
    
    def _get_connection(self) -> redis.Redis:
        """获取Redis连接"""
        if self._connection is None:
            try:
                self._connection = redis.Redis(
                    host=self.redis_host,
                    port=self.redis_port,
                    password=self.redis_password,
                    socket_timeout=self.socket_timeout,
                    # decode_responses=False  # 保持原始字节格式
                )
                # 测试连接
                self._connection.ping()
                logging.info(f"成功连接到Redis服务器 {self.redis_host}:{self.redis_port}")
            except Exception as e:
                logging.error(f"连接Redis失败: {e}")
                raise
        return self._connection
    
    def delete_keys_by_pattern(self, pattern: str, batch_size: int = 1000, 
                              dry_run: bool = False, confirm: bool = True) -> Tuple[int, List[str]]:
        """
        根据模式批量删除键
        
        Args:
            pattern: 键匹配模式 (如: 'user:*', '*cache*')
            batch_size: 每批次处理的键数量
            dry_run: 是否为测试运行（不实际删除）
            confirm: 是否需要用户确认
            
        Returns:
            Tuple[删除的键数量, 删除的键列表]
        """
        try:
            r = self._get_connection()
            
            # 首先扫描所有匹配的键
            matched_keys = self._scan_keys_by_pattern(pattern, batch_size)
            
            if not matched_keys:
                logging.info(f"未找到匹配模式 '{pattern}' 的键")
                return 0, []
            
            logging.info(f"找到 {len(matched_keys)} 个匹配模式 '{pattern}' 的键")
            
            # 显示前10个键作为预览
            preview_keys = matched_keys[:10]
            logging.info("预览将要删除的键:")
            for i, key in enumerate(preview_keys, 1):
                key_str = key.decode('utf-8') if isinstance(key, bytes) else str(key)
                logging.info(f"  {i}. {key_str}")
            
            if len(matched_keys) > 10:
                logging.info(f"  ... 还有 {len(matched_keys) - 10} 个键")
            
            # 用户确认
            if confirm and not dry_run:
                response = input(f"\n确定要删除这 {len(matched_keys)} 个键吗? (输入 'yes' 确认): ")
                if response.lower() != 'yes':
                    logging.info("操作已取消")
                    return 0, []
            
            if dry_run:
                logging.info("[DRY RUN] 模拟删除操作完成")
                return len(matched_keys), [key.decode('utf-8') if isinstance(key, bytes) else str(key) for key in matched_keys]
            
            # 批量删除键
            deleted_count = self._batch_delete_keys(matched_keys, batch_size)
            
            logging.info(f"成功删除 {deleted_count} 个键")
            return deleted_count, [key.decode('utf-8') if isinstance(key, bytes) else str(key) for key in matched_keys]
            
        except Exception as e:
            logging.error(f"删除键时发生错误: {e}")
            raise
    
    def delete_keys_by_list(self, key_list: List[str], batch_size: int = 1000,
                           dry_run: bool = False, confirm: bool = True) -> int:
        """
        根据键列表批量删除
        
        Args:
            key_list: 要删除的键列表
            batch_size: 每批次处理的键数量
            dry_run: 是否为测试运行
            confirm: 是否需要用户确认
            
        Returns:
            删除的键数量
        """
        try:
            if not key_list:
                logging.info("键列表为空")
                return 0
            
            r = self._get_connection()
            
            # 过滤存在的键
            existing_keys = []
            for key in key_list:
                if r.exists(key):
                    existing_keys.append(key)
            
            if not existing_keys:
                logging.info("指定的键都不存在")
                return 0
            
            logging.info(f"在 {len(key_list)} 个指定键中，找到 {len(existing_keys)} 个存在的键")
            
            # 显示要删除的键
            logging.info("将要删除的键:")
            for i, key in enumerate(existing_keys[:20], 1):
                logging.info(f"  {i}. {key}")
            
            if len(existing_keys) > 20:
                logging.info(f"  ... 还有 {len(existing_keys) - 20} 个键")
            
            # 用户确认
            if confirm and not dry_run:
                response = input(f"\n确定要删除这 {len(existing_keys)} 个键吗? (输入 'yes' 确认): ")
                if response.lower() != 'yes':
                    logging.info("操作已取消")
                    return 0
            
            if dry_run:
                logging.info("[DRY RUN] 模拟删除操作完成")
                return len(existing_keys)
            
            # 批量删除
            deleted_count = self._batch_delete_keys(existing_keys, batch_size)
            
            logging.info(f"成功删除 {deleted_count} 个键")
            return deleted_count
            
        except Exception as e:
            logging.error(f"删除键时发生错误: {e}")
            raise
    
    def delete_keys_by_prefix_suffix(self, prefix: str = "", suffix: str = "", 
                                   batch_size: int = 1000, dry_run: bool = False,
                                   confirm: bool = True) -> Tuple[int, List[str]]:
        """
        根据前缀和后缀删除键
        
        Args:
            prefix: 键前缀
            suffix: 键后缀
            batch_size: 每批次处理的键数量
            dry_run: 是否为测试运行
            confirm: 是否需要用户确认
            
        Returns:
            Tuple[删除的键数量, 删除的键列表]
        """
        if not prefix and not suffix:
            raise ValueError("前缀和后缀不能同时为空")
        
        # 构建匹配模式
        if prefix and suffix:
            pattern = f"{prefix}*{suffix}"
        elif prefix:
            pattern = f"{prefix}*"
        else:
            pattern = f"*{suffix}"
        
        logging.info(f"根据前缀'{prefix}'和后缀'{suffix}'构建匹配模式: {pattern}")
        return self.delete_keys_by_pattern(pattern, batch_size, dry_run, confirm)
    
    def _scan_keys_by_pattern(self, pattern: str, batch_size: int) -> List:
        """扫描匹配模式的所有键"""
        r = self._get_connection()
        matched_keys = []
        cursor = 0
        scan_count = 0
        
        logging.info(f"开始扫描匹配模式 '{pattern}' 的键")
        
        while True:
            cursor, keys = r.scan(cursor=cursor, match=pattern, count=batch_size)
            scan_count += 1
            
            if keys:
                matched_keys.extend(keys)
                logging.info(f"第{scan_count}次扫描，找到{len(keys)}个匹配的键，累计{len(matched_keys)}个")
            
            if cursor == 0:
                break
        
        logging.info(f"扫描完成，总共找到 {len(matched_keys)} 个匹配的键")
        return matched_keys
    
    def _batch_delete_keys(self, keys: List, batch_size: int) -> int:
        """批量删除键"""
        r = self._get_connection()
        total_deleted = 0
        
        # 分批删除
        for i in range(0, len(keys), batch_size):
            batch = keys[i:i + batch_size]
            try:
                deleted = r.delete(*batch)
                total_deleted += deleted
                logging.info(f"批次 {i//batch_size + 1}: 删除了 {deleted}/{len(batch)} 个键")
                
                # 添加小延迟避免对Redis造成太大压力
                if len(keys) > 10000:
                    time.sleep(0.01)
                    
            except Exception as e:
                logging.error(f"删除批次 {i//batch_size + 1} 时出错: {e}")
                continue
        
        return total_deleted
    
    def get_db_size(self) -> int:
        """获取数据库大小（键的总数）"""
        try:
            r = self._get_connection()
            return r.dbsize()
        except Exception as e:
            logging.error(f"获取数据库大小失败: {e}")
            return -1
    
    def close(self):
        """关闭连接"""
        if self._connection:
            self._connection.close()
            self._connection = None
            logging.info("Redis连接已关闭")


def delete_redis_keys_by_pattern(redis_host, redis_port, redis_password, pattern):
    """
    兼容旧版本的函数 - 删除 Redis 中匹配指定模式的所有键
    
    :param redis_host: Redis 主机地址
    :param redis_port: Redis 端口号
    :param redis_password: Redis 密码（如果没有密码，可以传入 None）
    :param pattern: 要匹配的键模式（例如 'user:*'）
    """
    deleter = RedisKeyDeleter(redis_host, redis_port, redis_password)
    try:
        deleted_count, deleted_keys = deleter.delete_keys_by_pattern(pattern, confirm=False)
        logging.info(f"删除了 {deleted_count} 个匹配模式 '{pattern}' 的键")
        return deleted_count
    except Exception as e:
        logging.error(f"删除操作失败: {e}")
        return 0
    finally:
        deleter.close()


def multi_server_delete(server_list, password, pattern):
    """
    轮询多个 Redis 服务器并执行删除操作

    :param server_list: 服务器配置列表，格式为 [(host, port), ...]
    :param password: Redis 密码
    :param pattern: 匹配模式
    """
    total_servers = len(server_list)
    overall_deleted = 0

    logging.info(f"开始对 {total_servers} 个 Redis 节点执行批量操作...")

    for host, port in server_list:
        logging.info("-" * 50)
        logging.info(f"正在处理节点 -> {host}:{port}")
        try:
            # 调用原有的兼容函数
            count = delete_redis_keys_by_pattern(host, port, password, pattern)
            overall_deleted += count
            logging.info(f"节点 {host}:{port} 处理完成，删除数量: {count}")
        except Exception as e:
            logging.error(f"处理节点 {host}:{port} 时发生意外错误: {e}")
            continue  # 一个节点失败，继续处理下一个

    logging.info("=" * 50)
    logging.info(f"所有节点处理完毕！总计删除键数量: {overall_deleted}")

# 示例调用
if __name__ == "__main__":
    # 1. 定义需要遍历的服务器列表 (Host, Port)
    redis_nodes = [
        ('172.16.70.21', 6379),
        ('172.16.70.21', 6382),
        ('172.16.70.21', 6381)
    ]

    # 2. 定义匹配模式
    # 提示：*1587404352* 会匹配任何包含该数字的键
    key_pattern = "*58153803*"

    # 3. 如果有统一密码请填写，没有则为 None
    redis_pwd = None

    # 4. 执行多服务器删除
    multi_server_delete(redis_nodes, redis_pwd, key_pattern)
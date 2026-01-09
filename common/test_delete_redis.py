#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Redis批量删除工具测试脚本
用于验证各种删除功能是否正常工作
"""

import redis
import logging
from delete_redis import RedisKeyDeleter

# 配置日志
logging.basicConfig(level=logging.INFO)

def setup_test_data():
    """创建测试数据"""
    print("=== 创建测试数据 ===")
    
    # Redis连接配置
    REDIS_HOST = '172.16.70.21'
    REDIS_PORT = 6379
    REDIS_PASSWORD = None
    
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
    
    # 创建测试键
    test_keys = {
        "test:user:1": "user1_data",
        "test:user:2": "user2_data", 
        "test:user:3": "user3_data",
        "test:cache:product:1": "product1_cache",
        "test:cache:product:2": "product2_cache",
        "test:session:abc123": "session_data_1",
        "test:session:def456": "session_data_2",
        "test:temp:file1": "temp_file_1",
        "test:temp:file2": "temp_file_2",
        "test:prefix_key_suffix": "test_data",
        "single_test_key": "single_data"
    }
    
    # 设置测试数据
    for key, value in test_keys.items():
        r.set(key, value)
        print(f"创建键: {key}")
    
    print(f"总共创建了 {len(test_keys)} 个测试键")
    return list(test_keys.keys())

def test_pattern_delete():
    """测试按模式删除"""
    print("\n=== 测试按模式删除 ===")
    
    deleter = RedisKeyDeleter('172.16.70.21', 6379, None)
    
    try:
        # 测试删除所有 test:user:* 键
        print("1. 测试删除 test:user:* 模式的键")
        deleted_count, deleted_keys = deleter.delete_keys_by_pattern(
            "test:user:*", dry_run=True, confirm=False
        )
        print(f"[DRY RUN] 找到 {deleted_count} 个匹配的键: {deleted_keys}")
        
        # 实际删除
        if deleted_count > 0:
            real_deleted, _ = deleter.delete_keys_by_pattern(
                "test:user:*", dry_run=False, confirm=False
            )
            print(f"实际删除了 {real_deleted} 个键")
        
    finally:
        deleter.close()

def test_list_delete():
    """测试按键列表删除"""
    print("\n=== 测试按键列表删除 ===")
    
    deleter = RedisKeyDeleter('172.16.70.21', 6379, None)
    
    try:
        # 测试删除指定键列表
        keys_to_delete = [
            "test:cache:product:1",
            "test:cache:product:2", 
            "non_existent_key"  # 不存在的键
        ]
        
        print(f"2. 测试删除指定键列表: {keys_to_delete}")
        deleted_count = deleter.delete_keys_by_list(
            keys_to_delete, dry_run=True, confirm=False
        )
        print(f"[DRY RUN] 将会删除 {deleted_count} 个键")
        
        # 实际删除
        if deleted_count > 0:
            real_deleted = deleter.delete_keys_by_list(
                keys_to_delete, dry_run=False, confirm=False
            )
            print(f"实际删除了 {real_deleted} 个键")
            
    finally:
        deleter.close()

def test_prefix_suffix_delete():
    """测试按前缀/后缀删除"""
    print("\n=== 测试按前缀/后缀删除 ===")
    
    deleter = RedisKeyDeleter('172.16.70.21', 6379, None)
    
    try:
        # 测试按前缀删除
        print("3. 测试按前缀 'test:session:' 删除")
        deleted_count, deleted_keys = deleter.delete_keys_by_prefix_suffix(
            prefix="test:session:", dry_run=True, confirm=False
        )
        print(f"[DRY RUN] 找到 {deleted_count} 个匹配前缀的键: {deleted_keys}")
        
        # 实际删除
        if deleted_count > 0:
            real_deleted, _ = deleter.delete_keys_by_prefix_suffix(
                prefix="test:session:", dry_run=False, confirm=False
            )
            print(f"实际删除了 {real_deleted} 个键")
        
        # 测试按后缀删除
        print("4. 测试按后缀 '_suffix' 删除")
        deleted_count, deleted_keys = deleter.delete_keys_by_prefix_suffix(
            suffix="_suffix", dry_run=True, confirm=False
        )
        print(f"[DRY RUN] 找到 {deleted_count} 个匹配后缀的键: {deleted_keys}")
        
        # 实际删除
        if deleted_count > 0:
            real_deleted, _ = deleter.delete_keys_by_prefix_suffix(
                suffix="_suffix", dry_run=False, confirm=False
            )
            print(f"实际删除了 {real_deleted} 个键")
            
    finally:
        deleter.close()

def test_cleanup():
    """清理剩余的测试数据"""
    print("\n=== 清理剩余测试数据 ===")
    
    deleter = RedisKeyDeleter('172.16.70.21', 6379, None)
    
    try:
        # 清理所有剩余的test:*键
        deleted_count, deleted_keys = deleter.delete_keys_by_pattern(
            "test:*", dry_run=False, confirm=False
        )
        print(f"清理了 {deleted_count} 个剩余的测试键")
        
        # 清理single_test_key
        remaining_keys = ["single_test_key"]
        deleted_count = deleter.delete_keys_by_list(
            remaining_keys, dry_run=False, confirm=False
        )
        print(f"清理了 {deleted_count} 个单独的测试键")
        
    finally:
        deleter.close()

def verify_database_state():
    """验证数据库状态"""
    print("\n=== 验证数据库状态 ===")
    
    deleter = RedisKeyDeleter('172.16.70.21', 6379, None)
    
    try:
        db_size = deleter.get_db_size()
        print(f"当前数据库大小: {db_size} 个键")
        
        # 检查是否还有测试键残留
        remaining_test_keys, _ = deleter.delete_keys_by_pattern(
            "test:*", dry_run=True, confirm=False
        )
        if remaining_test_keys > 0:
            print(f"警告: 还有 {remaining_test_keys} 个测试键残留")
        else:
            print("✓ 所有测试键已清理完毕")
            
    finally:
        deleter.close()

def main():
    """主测试函数"""
    print("Redis批量删除工具功能测试")
    print("=" * 50)
    
    try:
        # 1. 创建测试数据
        test_keys = setup_test_data()
        
        # 2. 验证初始状态
        verify_database_state()
        
        # 3. 测试各种删除功能
        test_pattern_delete()
        test_list_delete() 
        test_prefix_suffix_delete()
        
        # 4. 清理测试数据
        test_cleanup()
        
        # 5. 验证最终状态
        verify_database_state()
        
        print("\n" + "=" * 50)
        print("✓ 所有测试完成！")
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        logging.error(f"测试失败: {e}")

if __name__ == "__main__":
    main()
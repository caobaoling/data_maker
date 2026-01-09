#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Redis批量删除工具快速使用示例
展示常见使用场景
"""

from delete_redis import RedisKeyDeleter
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)

def main():
    """快速使用示例"""
    
    # Redis连接配置（修改为你的Redis服务器信息）
    REDIS_HOST = '172.16.70.21'
    REDIS_PORT = 6379
    REDIS_PASSWORD = None  # 如果有密码就填写密码字符串
    
    # 创建删除器实例
    deleter = RedisKeyDeleter(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)
    
    try:
        print("Redis批量删除工具 - 快速使用示例")
        print("=" * 50)
        
        # 获取当前数据库大小
        db_size = deleter.get_db_size()
        print(f"当前数据库大小: {db_size} 个键")
        
        # ==================== 使用示例 ====================
        
        # 示例1: 删除特定模式的键（测试运行）
        print("\n1. 删除匹配模式的键 (测试运行)")
        pattern = "1587401856*"  # 修改为你要删除的模式
        deleted_count, deleted_keys = deleter.delete_keys_by_pattern(
            pattern=pattern,
            dry_run=True,  # 测试运行，不实际删除
            confirm=False  # 不需要用户确认
        )
        print(f"找到 {deleted_count} 个匹配模式 '{pattern}' 的键")
        
        # 如果找到匹配的键，询问是否真正删除
        if deleted_count > 0:
            print("匹配的键:", deleted_keys[:5])  # 显示前5个
            if deleted_count > 5:
                print(f"... 还有 {deleted_count - 5} 个")
                
            # 实际删除（取消注释下面的代码来执行真正的删除）
            # confirm = input(f"确定要删除这 {deleted_count} 个键吗? (yes/no): ")
            # if confirm.lower() == 'yes':
            #     real_deleted, _ = deleter.delete_keys_by_pattern(
            #         pattern=pattern,
            #         dry_run=False,
            #         confirm=False
            #     )
            #     print(f"实际删除了 {real_deleted} 个键")
        
        # 示例2: 删除特定的键列表
        print("\n2. 删除指定的键列表")
        keys_to_delete = [
            "temp_key_1", 
            "temp_key_2",
            "old_cache_key",
            # 在这里添加更多要删除的键名
        ]
        
        deleted_count = deleter.delete_keys_by_list(
            key_list=keys_to_delete,
            dry_run=True,  # 测试运行
            confirm=False
        )
        print(f"在指定的 {len(keys_to_delete)} 个键中，将会删除 {deleted_count} 个存在的键")
        
        # 示例3: 按前缀删除键
        print("\n3. 按前缀删除键")
        prefix = "cache:"  # 修改为你的前缀
        deleted_count, deleted_keys = deleter.delete_keys_by_prefix_suffix(
            prefix=prefix,
            dry_run=True,
            confirm=False
        )
        print(f"找到 {deleted_count} 个以 '{prefix}' 开头的键")
        
        # 示例4: 按后缀删除键
        print("\n4. 按后缀删除键")
        suffix = "_temp"  # 修改为你的后缀
        deleted_count, deleted_keys = deleter.delete_keys_by_prefix_suffix(
            suffix=suffix,
            dry_run=True,
            confirm=False
        )
        print(f"找到 {deleted_count} 个以 '{suffix}' 结尾的键")
        
        # 示例5: 组合前缀和后缀
        print("\n5. 按前缀和后缀删除键")
        deleted_count, deleted_keys = deleter.delete_keys_by_prefix_suffix(
            prefix="session_",
            suffix="_expired",
            dry_run=True,
            confirm=False
        )
        print(f"找到 {deleted_count} 个以 'session_' 开头且以 '_expired' 结尾的键")
        
        print("\n" + "=" * 50)
        print("所有示例完成！")
        print("提示: 要执行实际删除，请修改脚本中的 dry_run=False")
        
    except Exception as e:
        print(f"执行过程中出现错误: {e}")
        logging.error(f"执行失败: {e}")
        
    finally:
        # 确保关闭连接
        deleter.close()
        print("连接已关闭")

if __name__ == "__main__":
    main()
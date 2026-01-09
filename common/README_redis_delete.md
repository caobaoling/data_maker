# Redis批量删除工具使用说明

## 功能概述

这是一个专为Redis设计的批量删除工具，提供多种删除方式，支持安全的删除操作和测试运行模式。

## 主要功能

### 1. 按模式删除键
- 支持Redis通配符模式匹配
- 例如：`user:*`、`*cache*`、`session_*_temp`

### 2. 按键列表删除
- 支持指定具体的键名列表进行删除
- 自动过滤不存在的键

### 3. 按前缀/后缀删除
- 可以指定键的前缀和/或后缀
- 内部转换为模式匹配

### 4. 安全特性
- **测试运行模式（Dry Run）**：先预览要删除的键，不实际删除
- **用户确认**：删除前需要用户确认
- **批量处理**：避免单次删除过多键造成Redis阻塞
- **进度显示**：显示删除进度和统计信息

## 使用方法

### 1. 交互式界面（推荐）

```bash
python delete_redis.py
```

运行后会显示菜单，按提示操作即可。

### 2. 编程调用

```python
from delete_redis import RedisKeyDeleter

# 创建删除器实例
deleter = RedisKeyDeleter(
    redis_host='172.16.70.21',
    redis_port=6379,
    redis_password=None
)

try:
    # 按模式删除（先测试运行）
    deleted_count, deleted_keys = deleter.delete_keys_by_pattern(
        pattern="user:*",
        dry_run=True,  # 测试运行
        confirm=False
    )
    print(f"将会删除 {deleted_count} 个键")
    
    # 实际删除
    if deleted_count > 0:
        actual_deleted, _ = deleter.delete_keys_by_pattern(
            pattern="user:*",
            dry_run=False,
            confirm=False
        )
        print(f"实际删除了 {actual_deleted} 个键")
        
finally:
    deleter.close()
```

### 3. 兼容旧版本调用

```bash
python delete_redis.py legacy
```

### 4. 运行示例

```bash
python delete_redis.py demo
```

## 类和方法说明

### RedisKeyDeleter 类

#### 初始化参数
- `redis_host`: Redis服务器地址
- `redis_port`: Redis端口号
- `redis_password`: Redis密码（可选）
- `socket_timeout`: 连接超时时间（默认30秒）

#### 主要方法

##### `delete_keys_by_pattern(pattern, batch_size=1000, dry_run=False, confirm=True)`
根据模式删除键
- `pattern`: 匹配模式（如 'user:*'）
- `batch_size`: 每批处理的键数量
- `dry_run`: 是否为测试运行
- `confirm`: 是否需要用户确认
- 返回：`(删除数量, 删除的键列表)`

##### `delete_keys_by_list(key_list, batch_size=1000, dry_run=False, confirm=True)`
根据键列表删除
- `key_list`: 要删除的键列表
- 其他参数同上
- 返回：删除的键数量

##### `delete_keys_by_prefix_suffix(prefix="", suffix="", batch_size=1000, dry_run=False, confirm=True)`
根据前缀和后缀删除键
- `prefix`: 键前缀
- `suffix`: 键后缀
- 其他参数同上
- 返回：`(删除数量, 删除的键列表)`

##### `get_db_size()`
获取当前数据库键的总数

##### `close()`
关闭Redis连接

## 使用示例

### 示例1：删除用户缓存
```python
# 删除所有用户缓存键
deleter.delete_keys_by_pattern("user_cache:*")
```

### 示例2：删除临时数据
```python
# 删除所有以temp开头的键
deleter.delete_keys_by_prefix_suffix(prefix="temp")
```

### 示例3：删除特定键列表
```python
# 删除指定的键
keys_to_delete = ["old_key1", "old_key2", "expired_session"]
deleter.delete_keys_by_list(keys_to_delete)
```

### 示例4：安全删除流程
```python
# 1. 先进行测试运行
count, keys = deleter.delete_keys_by_pattern("cache:*", dry_run=True)
print(f"将要删除 {count} 个缓存键")

# 2. 确认后实际删除
if count > 0 and input("确认删除? (yes/no): ") == "yes":
    actual_count, _ = deleter.delete_keys_by_pattern("cache:*", dry_run=False)
    print(f"实际删除了 {actual_count} 个键")
```

## 模式匹配语法

Redis支持以下通配符：
- `*` : 匹配任意数量的任意字符
- `?` : 匹配单个字符
- `[abc]` : 匹配方括号内的任意一个字符
- `[a-z]` : 匹配指定范围内的字符

### 常用模式示例
- `user:*` - 所有以"user:"开头的键
- `*cache*` - 包含"cache"的所有键
- `session_*_temp` - 以"session_"开头，"_temp"结尾的键
- `key_???` - 以"key_"开头后跟3个字符的键

## 安全建议

1. **务必先使用测试运行模式**：在执行实际删除前，先用 `dry_run=True` 查看要删除的键
2. **小批量测试**：对于大量数据，先用小范围的模式测试
3. **备份重要数据**：在执行大规模删除前，确保重要数据已备份
4. **生产环境谨慎操作**：在生产环境中使用时要格外小心
5. **监控删除进度**：观察日志输出，确保删除过程正常

## 注意事项

1. 删除操作不可逆，请谨慎使用
2. 大量键删除可能影响Redis性能，建议在低峰时段操作
3. 工具会自动分批处理，避免单次删除过多键
4. 支持中断操作（Ctrl+C）
5. 删除完成后会显示统计信息

## 错误处理

工具包含完善的错误处理机制：
- 自动重试连接失败
- 跳过删除失败的键并继续处理
- 详细的错误日志记录
- 优雅的中断处理

## 性能考虑

- 默认批量大小为1000个键，可根据需要调整
- 大量删除时会添加小延迟避免过度占用Redis资源
- 使用SCAN命令而非KEYS命令，对性能影响更小

---

**警告**: 此工具会永久删除Redis中的数据，使用前请确认操作的必要性和安全性！
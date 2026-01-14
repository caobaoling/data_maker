# Redis 多节点批量删除功能使用说明

## 功能概述

支持在多个Redis节点上同时执行批量删除操作，完全参考 `delete_redis.py` 中的 `multi_server_delete` 实现。

## Redis节点配置

系统预定义了三个Redis节点：

```javascript
[
  { host: '172.16.70.21', port: 6379, name: 'Redis-6379' },
  { host: '172.16.70.21', port: 6382, name: 'Redis-6382' },
  { host: '172.16.70.21', port: 6381, name: 'Redis-6381' }
]
```

## 使用流程

### 三步安全删除流程

#### **第一步：选择节点**

1. 在搜索框输入匹配模式（如：`appoint_*58153803*`）
2. 点击 **"多节点删除"** 按钮（橙色警告按钮）
3. 弹出节点选择对话框：
   - 显示当前匹配模式
   - 显示所有可用的Redis节点
   - 支持多选节点（勾选框）
   - 提供"全选"和"清空"快捷按钮
4. 选择要操作的节点
5. 点击 **"下一步：预览"** 按钮

#### **第二步：预览结果**

系统会在所有选中的节点上执行 **dry_run** 预览：

**显示内容：**
- ⚠️ 危险操作警告（红色提示框）
- 总计匹配键数统计
- 选中节点数量

**各节点统计表：**
| 节点 | 状态 | 匹配键数 | 错误信息 |
|------|------|----------|----------|
| Redis-6379 | 成功 | 150 | - |
| Redis-6382 | 成功 | 125 | - |
| Redis-6381 | 失败 | 0 | 连接超时 |

**预览键列表：**
- 显示前100个匹配的键名
- 来自所有节点（每个节点前20个）

**操作选项：**
- **上一步**：返回重新选择节点
- **取消**：放弃操作
- **确认删除**：执行实际删除

#### **第三步：确认删除**

点击"确认删除"后：
- 系统对所有选中节点执行 **dry_run=false** 真正删除
- 显示删除进度
- 返回删除结果：
  - 总删除键数
  - 成功节点数 / 失败节点数
  - 每个节点的详细结果

## 后端实现（参考 delete_redis.py）

### API端点

```
POST /api/redis/multi_node/delete_by_pattern
```

### 请求参数

```javascript
{
  "pattern": "appoint_*",         // 匹配模式
  "nodes": [                       // 节点列表（可选，默认所有）
    { "host": "...", "port": ... }
  ],
  "dry_run": true,                // true=预览，false=删除
  "password": null                 // Redis密码（可选）
}
```

### 响应数据

**预览模式（dry_run=true）：**
```javascript
{
  "code": "0",
  "msg": "在 3 个节点上找到 275 个匹配的键",
  "data": {
    "total_count": 275,
    "node_results": [
      {
        "node": "Redis-6379",
        "host": "172.16.70.21",
        "port": 6379,
        "success": true,
        "count": 150,
        "keys": ["key1", "key2", ...]  // 前20个
      },
      // ...其他节点
    ],
    "preview_keys": [...],  // 前100个键
    "has_more": true
  }
}
```

**删除模式（dry_run=false）：**
```javascript
{
  "code": "0",
  "msg": "成功在 3 个节点上删除 275 个键",
  "data": {
    "total_deleted": 275,
    "node_results": [
      {
        "node": "Redis-6379",
        "success": true,
        "count": 150
      },
      // ...其他节点
    ]
  }
}
```

## 核心特性

### 1. 容错机制
- ✅ 某个节点失败不影响其他节点
- ✅ 记录每个节点的成功/失败状态
- ✅ 显示详细的错误信息

### 2. 批量处理
- ✅ 每个节点使用 `batch_size=1000` 分批删除
- ✅ 避免阻塞Redis服务器
- ✅ 自动关闭每个节点的连接

### 3. 安全保障
- ✅ 第一步：选择节点
- ✅ 第二步：dry_run 预览
- ✅ 第三步：用户确认后执行
- ✅ 危险操作警告提示

### 4. 详细日志
后端日志示例：
```
INFO: [多节点预览] 模式: appoint_*, 节点数: 3, dry_run: True
INFO: [多节点预览] 正在处理节点 -> Redis-6379
INFO: [多节点预览] 节点 Redis-6379 处理完成，找到 150 个键
INFO: [多节点预览] 正在处理节点 -> Redis-6382
INFO: [多节点预览] 节点 Redis-6382 处理完成，找到 125 个键
INFO: [多节点预览] 完成！总共找到 275 个键
```

## 使用场景

### 场景1：清理用户缓存
```
模式: appoint_multi_redis_*58153803*
节点: 全选 (3个节点)
结果: 删除该用户在所有节点上的预约缓存
```

### 场景2：清理过期数据
```
模式: temp_data:2025*
节点: 全选
结果: 删除所有节点上2025年的临时数据
```

### 场景3：部分节点操作
```
模式: test:*
节点: 仅选择 Redis-6379
结果: 只在单个节点上删除测试数据
```

## 与 delete_redis.py 的对比

| 特性 | delete_redis.py | Web多节点工具 |
|------|----------------|---------------|
| 多节点支持 | ✅ multi_server_delete | ✅ |
| 容错机制 | ✅ try-except继续 | ✅ |
| dry_run预览 | ✅ | ✅ |
| 批量处理 | ✅ batch_size=1000 | ✅ |
| 节点统计 | ✅ 日志输出 | ✅ 表格展示 |
| 可视化选择 | ❌ | ✅ |
| 实时预览 | ❌ | ✅ |
| 无需改代码 | ❌ | ✅ |

## 注意事项

⚠️ **多节点删除是高危操作**
- 会同时影响多个Redis实例
- 删除操作不可恢复
- 请务必仔细检查预览结果

⚠️ **节点连接**
- 确保所有节点网络可达
- 注意节点密码配置
- 某节点失败会记录但继续执行

⚠️ **性能影响**
- 多节点同时操作会增加网络负载
- 建议在业务低峰期执行
- 大量键删除时注意监控

## 技术实现

### 后端核心代码

```python
@redis_bp.route('/multi_node/delete_by_pattern', methods=['POST'])
def multi_node_delete_by_pattern():
    # 遍历所有节点
    for node in nodes:
        try:
            deleter = RedisKeyDeleter(node_host, node_port, password)
            count, keys = deleter.delete_keys_by_pattern(
                pattern, batch_size=1000, dry_run, confirm=False
            )
            # 记录结果
            node_results.append({
                'node': node_name,
                'success': True,
                'count': count
            })
        except Exception as e:
            # 容错处理
            node_results.append({
                'node': node_name,
                'success': False,
                'error': str(e)
            })
            continue  # 继续处理下一个节点
```

### 前端核心流程

```javascript
// 第一步：选择节点
handleMultiNodeDelete()
  → 显示节点选择对话框
  → 用户勾选节点

// 第二步：预览
handlePreviewMultiNode()
  → API: { dry_run: true }
  → 显示各节点统计
  → 显示预览键列表

// 第三步：确认删除
handleConfirmMultiNodeDelete()
  → API: { dry_run: false }
  → 显示删除结果
  → 刷新统计
```

---

## 快速开始

1. 访问：http://localhost:3000/redis/tool
2. 输入匹配模式
3. 点击"多节点删除"按钮
4. 选择要操作的节点
5. 查看预览结果
6. 确认后执行删除

现在可以安全地在多个Redis节点上批量删除数据了！🎉

# 📡 API接口文档

## 📋 基础信息

**Base URL (开发环境)**: `http://localhost:5001`
**Base URL (生产环境)**: `http://your-domain.com`
**Content-Type**: `application/json`

---

## 🔑 通用响应格式

### 成功响应

```json
{
  "code": "10000",
  "message": "操作成功",
  "data": {}
}
```

### 错误响应

```json
{
  "code": "40000",
  "message": "参数错误",
  "data": null
}
```

### 状态码说明

| Code | 说明 |
|------|------|
| 10000 | 成功 |
| 40000 | 客户端错误（参数错误、业务错误） |
| 50000 | 服务器错误 |

---

## 📚 课程预约 API

### 1. 添加普通话预约

**接口**: `POST /api/appoint/add_cn`

**请求参数**:

```json
{
  "stu_id": "12345678",
  "t_id": "350012781",
  "start_time": "2026-01-16 09:00:00",
  "end_time": "2026-01-16 09:30:00",
  "date_time": "20260116_19",
  "course_type": "31",
  "point_type": "pthpoint",
  "use_point": "buy",
  "status": "on",
  "course_id": "1406031",
  "course_top_id": "1400011",
  "course_sub_id": "1406021"
}
```

**参数说明**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| stu_id | string | 是 | 学生ID |
| t_id | string | 是 | 教师ID（普通话参考: 350012781） |
| start_time | string | 是 | 开始时间（格式: YYYY-MM-DD HH:mm:ss） |
| end_time | string | 是 | 结束时间（自动计算，比开始时间晚30分钟） |
| date_time | string | 是 | 时间编号（格式: YYYYMMDD_时间段） |
| course_type | string | 是 | 课程类型（31=普通话） |
| point_type | string | 是 | 点数类型（pthpoint=普通话点数） |
| use_point | string | 是 | 课程性质（buy=付费课, free=体验课） |
| status | string | 是 | 预约状态（on=正常, cancel=取消） |
| course_id | string | 是 | 课程ID |
| course_top_id | string | 是 | 课程顶级ID |
| course_sub_id | string | 是 | 课程子级ID |

**响应示例**:

```json
{
  "code": "10000",
  "message": "预约创建成功",
  "res": {
    "id": "577708965"
  }
}
```

---

### 2. 添加英语预约

**接口**: `POST /api/appoint/add_en`

**请求参数**: 同添加普通话预约，区别如下:

| 参数 | 值 |
|------|-----|
| course_type | "1" |
| point_type | "point" |
| t_id | "2821" (参考) |
| course_id | "1166431" (付费课) 或 "821221" (体验课) |

---

### 3. 查询预约列表

**接口**: `GET /api/appoint/list`

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | number | 否 | 页码（默认1） |
| pageSize | number | 否 | 每页数量（默认20） |
| stuId | string | 否 | 学生ID |
| tId | string | 否 | 教师ID |
| status | string | 否 | 状态（on/end/s_absent/t_absent/cancel） |
| courseType | string | 否 | 课程类型（1/31） |
| category | string | 否 | 课程种类（ph_free/ph_buy/ea_buy等） |
| startDate | string | 否 | 开始日期（YYYY-MM-DD） |
| endDate | string | 否 | 结束日期（YYYY-MM-DD） |

**响应示例**:

```json
{
  "code": "10000",
  "message": "查询成功",
  "data": {
    "list": [
      {
        "id": "577708964",
        "s_id": "12345678",
        "t_id": "2821",
        "start_time": "2026-01-16 09:00:00",
        "end_time": "2026-01-16 09:30:00",
        "status": "on",
        "course_type": "1",
        "point_type": "point",
        "category": "ph_buy",
        "date_time": "20260116_19"
      }
    ],
    "total": 100,
    "page": 1,
    "pageSize": 20
  }
}
```

---

### 4. 修改预约状态

**接口**: `POST /api/appoint/update_status`

**请求参数**:

```json
{
  "id": "577708964",
  "status": "end"
}
```

**参数说明**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 预约ID |
| status | string | 是 | 新状态（on/end/s_absent/t_absent/cancel） |

**状态值说明**:

| 值 | 说明 |
|----|------|
| on | 正常 |
| end | 已结束 |
| s_absent | 学生缺席 |
| t_absent | 教师缺席 |
| cancel | 取消 |

**响应示例**:

```json
{
  "code": "10000",
  "message": "状态修改成功",
  "data": {
    "id": "577708964",
    "status": "end"
  }
}
```

---

### 5. 预约打星

**接口**: `POST /api/appoint/add_star`

**请求参数**:

```json
{
  "stu_id": "12345678",
  "appoint_id": "577708964",
  "star_num": 5
}
```

**参数说明**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| stu_id | string | 是 | 学生ID |
| appoint_id | string | 是 | 预约ID |
| star_num | number | 是 | 星数（1-5） |

---

## 🔧 Redis工具 API

### 批量删除Redis键

**接口**: `POST /api/redis/delete`

**请求参数**:

```json
{
  "host": "172.16.70.21",
  "port": 6379,
  "password": "",
  "mode": "pattern",
  "pattern": "user:*",
  "prefix": "",
  "suffix": "",
  "dry_run": true,
  "batch_size": 100
}
```

**参数说明**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| host | string | 是 | Redis主机地址 |
| port | number | 是 | Redis端口 |
| password | string | 否 | Redis密码 |
| mode | string | 是 | 删除模式（pattern/prefix_suffix） |
| pattern | string | 否 | 匹配模式（mode=pattern时必填） |
| prefix | string | 否 | 前缀（mode=prefix_suffix时必填） |
| suffix | string | 否 | 后缀（mode=prefix_suffix时必填） |
| dry_run | boolean | 否 | 是否测试运行（默认true） |
| batch_size | number | 否 | 批量大小（默认100） |

**响应示例**:

```json
{
  "code": "10000",
  "message": "删除成功",
  "data": {
    "deleted_count": 150,
    "keys_sample": ["user:123", "user:456", "..."]
  }
}
```

---

## 🤖 AI外教 API

### 1. 添加AI点数

**接口**: `POST /api/ai/add_point`

**请求参数**:

```json
{
  "user_id": "12345678",
  "point": 100,
  "expire_days": 300
}
```

**参数说明**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | string | 是 | 用户ID |
| point | number | 否 | 点数（默认100） |
| expire_days | number | 否 | 有效天数（默认300） |

---

### 2. 添加兑换码

**接口**: `POST /api/ai/add_exchange_code`

**请求参数**:

```json
{
  "user_id": "12345678"
}
```

---

### 3. 清空学习计划

**接口**: `POST /api/ai/clear_plan`

**请求参数**:

```json
{
  "user_id": "12345678"
}
```

**响应示例**:

```json
{
  "code": "10000",
  "message": "学习计划清空成功",
  "data": {
    "deleted_tables": 12,
    "affected_rows": 156
  }
}
```

---

## 🧚 精灵系统 API

### 1. 修改精灵等级

**接口**: `POST /api/elf/change_level`

**请求参数**:

```json
{
  "user_id": "12345678",
  "level": 10
}
```

**参数说明**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | string | 是 | 用户ID |
| level | number | 是 | 目标等级（1-40） |

---

### 2. 添加星星

**接口**: `POST /api/elf/add_star`

**请求参数**:

```json
{
  "user_id": "12345678",
  "star_num": 5
}
```

---

### 3. 查询精灵任务

**接口**: `POST /api/elf/query_task`

**请求参数**:

```json
{
  "user_id": "12345678"
}
```

**响应示例**:

```json
{
  "code": "10000",
  "message": "查询成功",
  "data": {
    "tasks": [
      {
        "user_task_id": "123456",
        "task_name": "完成课程",
        "status": "进行中",
        "progress": "3/5"
      }
    ]
  }
}
```

---

### 4. 删除精灵任务

**接口**: `POST /api/elf/delete_task`

**请求参数**:

```json
{
  "user_id": "12345678"
}
```

**响应示例**:

```json
{
  "code": "10000",
  "message": "任务删除成功",
  "data": {
    "deleted_count": 15
  }
}
```

---

### 5. 管理排行榜

**接口**: `POST /api/elf/manage_rank`

**请求参数**:

```json
{
  "action": "reset_week"
}
```

**参数说明**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| action | string | 是 | 操作类型（reset_week=重置周排行榜） |

---

## 🧪 测试工具

### Postman测试

导入以下环境变量:

```json
{
  "base_url": "http://localhost:5001",
  "stu_id": "12345678",
  "t_id_cn": "350012781",
  "t_id_en": "2821"
}
```

### cURL示例

```bash
# 健康检查
curl http://localhost:5001/api/health

# 添加预约
curl -X POST http://localhost:5001/api/appoint/add_cn \
  -H "Content-Type: application/json" \
  -d '{
    "stu_id": "12345678",
    "t_id": "350012781",
    "start_time": "2026-01-16 09:00:00",
    "end_time": "2026-01-16 09:30:00",
    "date_time": "20260116_19",
    "course_type": "31",
    "use_point": "buy"
  }'

# 查询预约列表
curl "http://localhost:5001/api/appoint/list?stuId=12345678&page=1&pageSize=10"
```

---

## 📝 注意事项

1. **时间格式**: 所有时间参数使用 `YYYY-MM-DD HH:mm:ss` 格式
2. **时间限制**: 预约时间只能选择整点（XX:00:00）或半点（XX:30:00）
3. **状态变更**: 调用外部接口，需确保外部API可访问
4. **Redis操作**: 建议先用 `dry_run=true` 测试，确认无误后再实际删除
5. **错误处理**: 所有API都返回统一格式，注意检查 `code` 字段

---

## 🔗 相关链接

- [项目README](README.md)
- [Docker部署指南](DOCKER.md)
- [项目详细文档](CLAUDE.md)

---

<div align="center">

**📡 API文档持续更新中...**

</div>

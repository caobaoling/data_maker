# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个用于测试数据生成和管理的 Python 工具集,主要用于教育平台的数据操作。项目包含多个独立的脚本模块,用于处理用户预约、订单、精灵系统、AI外教等数据。

## 技术栈

- **语言**: Python 3.x
- **数据库**: MySQL (pymysql)
- **缓存**: Redis
- **HTTP客户端**: requests
- **虚拟环境**: venv

## 核心架构

### 目录结构说明

```
dataMaker/
├── common/          # 公共工具模块
│   ├── db_connect.py         # 数据库连接和基础CRUD操作
│   ├── db_utils.py           # 配置文件读取工具
│   ├── api_client.py         # HTTP请求封装(GET/POST)
│   ├── delete_redis.py       # Redis批量删除工具(核心工具)
│   ├── search_redis.py       # Redis查询工具
│   ├── execute_batch.py      # 通用批量数据库操作执行器(新增)
│   ├── elf_level_config.py   # 精灵等级配置数据
│   ├── test_delete_redis.py  # Redis删除测试脚本
│   └── quick_delete_example.py # Redis快速删除示例
├── config/          # 配置文件
│   └── database.json         # 数据库连接配置(host/port/user/password)
├── aiTeacher/       # AI外教相关操作
│   ├── ai_add_point.py         # 添加AI点数
│   ├── ai_add_exchange_code.py # 添加兑换码
│   └── ai_del_studyplan_all.py # 清空学习计划(新增)
├── orders/          # 订单管理
│   └── add_order.py          # 创建订单
├── appoint/         # 课程预约管理
│   ├── add_appoint_cn.py       # 添加普通话预约
│   ├── add_appoint_en.py       # 添加英语预约
│   ├── appoint_add_star.py     # 预约数据打星标
│   ├── change_appoint_status.py # 修改预约状态
│   └── search_appoints.py      # 查询预约信息
├── elf/             # 精灵系统管理
│   ├── elf_change_level.py    # 修改精灵等级
│   ├── elf_add_star.py         # 精灵数据打星标
│   ├── elf_create_task.py      # 创建精灵任务(新增)
│   ├── elf_del_task.py         # 删除精灵任务(新增)
│   ├── elf_rank.py             # 精灵排行榜数据管理(新增)
│   └── elf_create_endclass_java.py # 精灵结课Java脚本
├── picturebook/     # 绘本系统管理(新增模块)
│   └── pb_del_data.py          # 删除绘本数据
└── tools/           # 其他辅助工具
    ├── del_redis.py            # Redis删除工具
    ├── high_risk_user_device.py # 高风险用户设备管理
    ├── url_unquote.py          # URL解码工具
    ├── add_assets.py           # 添加资产
    ├── number_formatter.py     # 数字格式化工具
    └── details wordcloud2Svg.py # 词云转SVG工具
```

### 数据库架构

项目使用 MySQL 数据库,连接配置统一在 `config/database.json` 中管理。主要操作的数据库包括:

- `talkplatform_game`: 精灵系统相关表
- `talkplatform_order_consumer`: 订单系统
- `talkplatform_appointone_consumer`: 预约系统
- `talkplatform_task`: 任务系统(精灵任务等)
- `talkplatform_ai_teacher`: AI外教学习计划系统
- `talkplatform_ai_pbook`: 绘本系统
- `point`: 点数资产系统

### 核心模块说明

#### 1. 数据库连接层 (common/db_connect.py)

提供统一的数据库操作接口:

- `create_connection()`: 创建数据库连接
- `execute_query()`: 执行查询语句
- `execute_non_query()`: 执行非查询语句(INSERT/UPDATE/DELETE)
- `insert_data()`, `update_data()`, `delete_data()`, `select_data()`: 封装的CRUD操作

**使用示例**:
```python
from common.db_connect import create_connection, select_data
conn = create_connection()
results = select_data(conn, 'user_table', columns='*', condition='user_id=123')
conn.close()
```

#### 2. Redis 操作工具 (common/delete_redis.py)

这是项目中最完善的工具类,提供安全的 Redis 批量删除功能:

**核心类**: `RedisKeyDeleter`

**关键方法**:
- `delete_keys_by_pattern(pattern, batch_size, dry_run, confirm)`: 按模式删除
- `delete_keys_by_list(key_list)`: 按键列表删除
- `delete_keys_by_prefix_suffix(prefix, suffix)`: 按前缀/后缀删除

**安全特性**:
- 支持 `dry_run` 模式先预览不实际删除
- 需要用户确认才执行删除
- 批量处理避免阻塞 Redis
- 详细的日志输出

**使用模式**:
```python
deleter = RedisKeyDeleter('host', 6379, password)
# 先测试运行
count, keys = deleter.delete_keys_by_pattern("user:*", dry_run=True)
# 确认后实际删除
count, keys = deleter.delete_keys_by_pattern("user:*", dry_run=False)
deleter.close()
```

#### 3. HTTP 客户端 (common/api_client.py)

提供简单的 HTTP 请求封装:
- `send_request_get(url, params)`: GET 请求
- `send_request_post(url, params)`: POST 请求

#### 4. 配置管理 (common/db_utils.py)

- `load_config()`: 从 `config/database.json` 读取数据库配置

#### 5. 批量数据库操作工具 (common/execute_batch.py) **[新增核心工具]**

提供统一的批量数据库操作执行器,支持事务回滚和详细日志:

**核心函数**: `execute_batch_op(connection, queries, param_value)`

**参数说明**:
- `connection`: 数据库连接对象
- `queries`: SQL语句列表,格式为 `[(sql, param_name), ...]`
- `param_value`: 需要传入的参数值(如 user_id 或 time_key)

**特性**:
- 自动事务管理:成功提交,失败回滚
- 支持带占位符(%s)和不带占位符的SQL混合执行
- 详细的日志记录(每条SQL截取前60字符避免刷屏)
- 统一的异常处理

**使用示例**:
```python
from common.db_connect import create_connection
from common.execute_batch import execute_batch_op

conn = create_connection()
delete_queries = [
    ("DELETE FROM user_table WHERE user_id = %s", "user_id"),
    ("DELETE FROM user_stats WHERE user_id = %s", "user_id"),
    ("UPDATE global_config SET updated = NOW();", "none")  # 无参数SQL
]
execute_batch_op(conn, delete_queries, 123456)
conn.close()
```

**应用场景**:
- 精灵任务批量删除 (`elf/elf_del_task.py`)
- 绘本数据清理 (`picturebook/pb_del_data.py`)
- AI外教学习计划清空 (`aiTeacher/ai_del_studyplan_all.py`)
- 精灵排行榜数据重置 (`elf/elf_rank.py`)

### 业务模块说明

#### appoint/ - 课程预约

- `add_appoint_cn.py`: 添加普通话课程预约
- `add_appoint_en.py`: 添加英语课程预约
- `appoint_add_star.py`: 预约数据打星标
- `change_appoint_status.py`: 修改预约状态
- `search_appoints.py`: 查询预约信息

**关键配置**:
- 普通话课程: `course_type=31`, `point_type=pthpoint`, `t_id=350012781`
- 英语课程: `course_type=1`, `point_type=point`, `t_id=2821`
- 课程时间计算逻辑: 30分钟一节课,时间段编号计算方式为 `hour * 2 + 1` (半点+1)

#### orders/ - 订单管理

- `add_order.py`: 创建用户订单
- API: `http://172.16.16.97/talkplatform_order_consumer/v1/order/add`

#### elf/ - 精灵系统

- `elf_change_level.py`: 修改精灵等级
- `elf_add_star.py`: 精灵数据打星标
- `elf_create_task.py`: 创建精灵任务(查询周期性任务)
- `elf_del_task.py`: 清空精灵任务(批量删除用户的game_system任务)
- `elf_rank.py`: 精灵排行榜数据管理(删除周数据+重置状态)
- `elf_create_endclass_java.py`: 精灵结课Java脚本
- 使用 `common.elf_level_config.ElfLevelData` 获取等级配置数据

**任务系统API**:
- 查询周期性任务: `http://172.16.16.36/talkplatform_task_consumer/task/user_task/v1/front/query_in_cycle_user_task_list`
- 参数: `biz_category=game_system`, `task_biz_category_list=elf_week_task,elf_month_task`

**排行榜数据管理** (`elf_rank.py`):
- 自动计算上周的时间键(格式: `YYYY-wWW`, 如 `2025-w09`)
- 删除 `user_rank_round`, `rank_round`, `rank_round_reward` 表的周数据
- 重置 `robot_rank.use_status=0` 和 `user_rank_level.use_flag=0`

#### aiTeacher/ - AI外教

- `ai_add_exchange_code.py`: 为用户添加兑换码
- `ai_add_point.py`: 为用户添加AI点数(插入 `point.user_assets` 表)
- `ai_del_studyplan_all.py`: 清空用户学习计划(删除12个相关表的数据)
- API: `http://172.16.16.36/talkplatform_leads_consumer/leads/third/tiktok/v1/front/user_exchange_order`

**AI点数系统**:
- SKU类型: `sku_id=113`, `sku_type='ai_teach'`
- 默认添加100点,有效期300天

**学习计划清理** (`ai_del_studyplan_all.py`):
- 清理表: `user_info`, `user_lesson_consume_record`, `user_lesson_exam_info`, `user_report`, `user_test_analysis`, `user_statistics_gold_coin_log`, `user_week_statistics`, `user_week_plan`, `user_timetable_finish_record`, `user_statistics`, `user_timetable`, `user_update_log`

#### picturebook/ - 绘本系统 **[新增模块]**

- `pb_del_data.py`: 删除用户绘本数据(清理12个相关表)

**数据清理范围**:
- 基础表: `user_info`, `user_weekly_statistics`, `weekly_report`, `reading_setting`
- 分表(按user_id后两位): `user_settlement_XX`, `user_report_XX`, `user_practice_XX`, `user_game_asset_record_XX`, `picture_book_reading_plan_XX`, `picture_book_reading_plan_3`
- 统计表: `user_daily_statistics_info`, `course_package_reading_plan`

**分表规则**: `int(str(user_id)[-2:])` 取用户ID后两位作为表后缀

## 开发实践

### 环境准备

```bash
# 激活虚拟环境
# Windows:
venv\Scripts\activate

# 安装依赖(如果有requirements.txt)
pip install pymysql redis requests
```

### 运行脚本

项目中的脚本通常设计为独立运行,修改脚本中的参数后直接执行:

```bash
python appoint/add_appoint_cn.py
python elf/elf_change_level.py
python common/delete_redis.py
```

### 配置管理

在修改数据库连接信息时,编辑 `config/database.json`:
```json
{
    "host": "172.16.70.20",
    "port": 3306,
    "user": "rd_user",
    "password": "NTHXDF7czYwi"
}
```

### 代码风格

- 文件头注释包含: 文件名、作者(bao0)、创建日期、描述
- 使用 logging 模块记录日志而非简单的 print
- 变量名使用下划线命名法 (snake_case)
- 数据库连接需要显式关闭

### 安全注意事项

1. **Redis 删除操作**: 始终使用 `delete_redis.py` 的 `dry_run=True` 模式先预览,确认后再实际删除
2. **数据库操作**: 避免在生产数据库上直接运行测试脚本
3. **敏感信息**: `config/database.json` 包含敏感凭据,不应提交到版本控制

## API 端点

项目中使用的主要内部 API:

- 订单服务: `http://172.16.16.97/talkplatform_order_consumer/v1/order/add`
- 预约服务: `http://172.16.16.97/talkplatform_appointone_consumer/v1/appoint/add`
- AI外教服务: `http://172.16.16.36/talkplatform_leads_consumer/leads/third/tiktok/v1/front/user_exchange_order`

## Redis 连接

- 生产环境: `172.16.70.21:6379` (无密码)

## 常见任务

### 创建测试预约

1. 编辑 `appoint/add_appoint_cn.py`
2. 修改 `t_id`, `stu_id`, `start_time` 等参数
3. 运行脚本

### 批量删除 Redis 键

1. 使用 `common/delete_redis.py` 的 `RedisKeyDeleter` 类
2. 先用 `dry_run=True` 预览
3. 确认后实际删除

### 修改精灵等级

1. 编辑 `elf/elf_change_level.py`
2. 修改 `user_id` 和 `level` 参数
3. 运行脚本更新数据库

### 清空精灵任务 **[新增]**

1. 编辑 `elf/elf_del_task.py` 修改 `user_id`
2. 自动查询 `biz_category='game_system'` 的任务
3. 批量删除6个相关表的数据(user_task, user_task_award等)

### 重置精灵排行榜 **[新增]**

1. 运行 `elf/elf_rank.py`
2. 自动计算上周时间键并删除对应数据
3. 重置机器人和用户的使用状态

### 清空用户学习计划 **[新增]**

1. 编辑 `aiTeacher/ai_del_studyplan_all.py` 修改 `user_id`
2. 运行脚本清理12个相关表
3. 适用于测试环境重置用户学习数据

### 删除绘本数据 **[新增]**

1. 编辑 `picturebook/pb_del_data.py` 修改 `user_id`
2. 运行脚本清理12个绘本相关表
3. 自动处理分表逻辑(按user_id后两位)

### 添加AI点数 **[新增]**

1. 编辑 `aiTeacher/ai_add_point.py` 修改 `user_id`
2. 默认添加100点AI外教点数,有效期300天
3. SKU类型: `ai_teach`

## 重要模式和技巧

### 数据库分表规则

项目中多个系统使用分表策略,统一规则:

```python
# 取用户ID后两位作为表后缀
suffix = int(str(user_id)[-2:])
table_name = f"user_data_{suffix}"
```

**适用系统**:
- 绘本系统: `user_settlement_XX`, `user_report_XX`, `user_practice_XX` 等
- 精灵任务: `user_task_XX`, `user_award_XX`

### 批量数据操作最佳实践

使用 `execute_batch.py` 进行批量操作:

**优势**:
- 事务安全:失败自动回滚
- 日志完善:每步操作可追踪
- 代码复用:避免重复的异常处理

**标准模板**:
```python
from common.db_connect import create_connection
from common.execute_batch import execute_batch_op

def main():
    user_id = 12345678
    queries = [
        ("DELETE FROM table1 WHERE user_id = %s", "user_id"),
        ("DELETE FROM table2 WHERE user_id = %s", "user_id"),
        ("UPDATE global_stats SET count = count - 1;", "none")  # 不需参数
    ]
    conn = create_connection()
    execute_batch_op(conn, queries, user_id)
    conn.close()
```

### 时间键计算

精灵排行榜使用周时间键 (`YYYY-wWW`), 自动计算逻辑见 `elf/elf_rank.py`:

```python
def get_last_sunday_of_previous_week():
    today = datetime.date.today()
    days_to_sunday = 7 - today.isoweekday()
    current_sunday = today + datetime.timedelta(days=days_to_sunday)
    last_sunday = current_sunday - datetime.timedelta(days=7)
    return last_sunday.strftime("%Y-w%V")
```

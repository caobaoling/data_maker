# 📊 DataMaker - 测试数据管理平台

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Vue](https://img.shields.io/badge/Vue-3.4+-green.svg)](https://vuejs.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-lightgrey.svg)](https://flask.palletsprojects.com/)
[![Element Plus](https://img.shields.io/badge/Element%20Plus-2.5+-409EFF.svg)](https://element-plus.org/)
[![Docker](https://img.shields.io/badge/Docker-支持-2496ED.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**快速、高效、易用的教育平台测试数据管理工具**

[功能特性](#-功能特性) • [快速开始](#-快速开始) • [使用文档](#-使用文档) • [技术栈](#-技术栈) • [项目结构](#-项目结构)

</div>

---

## 📖 项目简介

DataMaker 是一个专为教育平台设计的测试数据生成和管理工具，提供了 Web 可视化界面和 Python 脚本两种操作方式。通过简洁的界面和强大的功能，帮助测试人员和开发人员快速创建和管理各类测试数据。

### 🎯 核心价值

- 🚀 **提升效率**: Web界面操作，无需编写代码即可生成测试数据
- 🔧 **灵活扩展**: 保留Python脚本工具，支持批量操作和自动化
- 📦 **一键部署**: Docker容器化，开箱即用
- 🎨 **现代化UI**: 基于Element Plus，界面美观易用
- 🔒 **数据安全**: 直接调用业务API，保证数据一致性

---

## ✨ 功能特性

### 📚 课程预约管理
- ✅ **添加预约**: 支持普通话和英语课程预约创建
  - 时间选择限制（整点/半点）
  - 智能教材推荐
  - 自动计算结束时间和时间编号
  - JSON预览功能
- ✅ **预约列表**: 多条件查询、分页展示、状态变更
- ✅ **预约打星**: 课程评价星标管理

### 🧚 精灵系统管理
- ✅ **等级管理**: 修改精灵等级（支持经验值自动计算）
- ✅ **星星管理**: 添加精灵星星奖励
- ✅ **任务管理**: 查询和删除精灵任务
- ✅ **结课功能**: 批量结课操作
- ✅ **排行榜管理**: 重置周排行榜数据

### 🤖 AI外教管理
- ✅ **添加点数**: 为用户添加AI外教点数
- ✅ **兑换码管理**: 生成和使用兑换码
- ✅ **清空学习计划**: 重置用户AI外教学习进度

### 🔧 Redis工具箱
- ✅ **批量删除**: 按模式、前缀/后缀批量删除Redis键
- ✅ **安全模式**: Dry-run预览，二次确认
- ✅ **查询工具**: 快速查找Redis键

### 📝 Python脚本工具集
- 保留所有原有Python脚本，支持批量操作和自动化任务
- 完善的工具类封装（数据库、Redis、HTTP客户端）

---

## 🚀 快速开始

### 📋 环境要求

**使用Docker（推荐）:**
- Docker 20.10+
- Docker Compose 2.0+

**本地开发:**
- Python 3.11+
- Node.js 18+
- MySQL 5.7+ (可选，用于数据库直连)
- Redis 6+ (可选，用于Redis工具)

---

### 🐳 方式一：Docker 一键启动（推荐）

```bash
# 1. 克隆项目
git clone https://github.com/caobaoling/data_maker.git
cd data_maker

# 2. 启动所有服务
docker-compose up -d

# 3. 查看服务状态
docker-compose ps

# 4. 查看日志
docker-compose logs -f
```

**访问地址:**
- 🌐 前端界面: http://localhost:8080
- 🔌 后端API: http://localhost:5001/api/health

**停止服务:**
```bash
docker-compose down
```

---

### 💻 方式二：本地开发运行

#### 1️⃣ 启动后端服务

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（可选但推荐）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动Flask服务
python app.py
```

✅ 后端运行在: http://localhost:5001

#### 2️⃣ 启动前端服务

```bash
# 打开新终端，进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

✅ 前端运行在: http://localhost:3000

---

## 📖 使用文档

### 🎮 快速上手

#### 1. 添加课程预约

1. 访问 http://localhost:3000/appoint/add
2. 选择课程类型（普通话/英语）
3. 填写学生ID和教师ID
4. 选择开始时间（只能选择整点或半点）
5. 选择课程性质（体验课/付费课）
6. 点击"创建预约"

💡 **提示**:
- 普通话教师ID参考: `350012781`
- 英语教师ID参考: `2821`
- 时间限制：只能选择 XX:00:00 或 XX:30:00

#### 2. 管理预约列表

1. 访问 http://localhost:3000/appoint/list
2. 使用筛选条件查询预约
3. 点击"变更状态"修改预约状态
4. 支持状态：正常、已结束、学生缺席、教师缺席、取消

#### 3. 精灵系统操作

**修改等级:**
- 访问 http://localhost:3000/elf/change-level
- 输入用户ID和目标等级
- 系统自动计算所需经验值

**管理任务:**
- 查询任务: http://localhost:3000/elf/query-task
- 删除任务: http://localhost:3000/elf/del-task

#### 4. Redis批量操作

1. 访问 http://localhost:3000/redis/tool
2. 选择删除模式（模式匹配/前缀后缀）
3. 先使用"测试运行"预览
4. 确认无误后执行删除

---

## 🔧 配置说明

### API端点配置

后端配置文件: `backend/api/*.py`

主要API端点:
```python
# 预约API
APPOINT_ADD_API = "http://172.16.16.97/talkplatform_appointone_consumer/v1/appoint/add"
APPOINT_UPDATE_API = "http://172.16.16.97/talkplatform_appointone_consumer/v1/appoint/update"

# 精灵任务API
TASK_API = "http://172.16.16.36/talkplatform_task_consumer/task/user_task/v1/front/query_in_cycle_user_task_list"
```

### 前端代理配置

开发模式下，前端通过Vite代理转发API请求:

文件: `frontend/vite.config.js`

```javascript
server: {
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://localhost:5001',
      changeOrigin: true
    }
  }
}
```

---

## 🏗️ 技术栈

### 后端技术

| 技术 | 版本 | 说明 |
|------|------|------|
| Python | 3.11+ | 主要编程语言 |
| Flask | 3.0.0 | Web框架 |
| Flask-CORS | 4.0.0 | 跨域支持 |
| pymysql | 1.1.0 | MySQL数据库驱动 |
| redis | 5.0.1 | Redis客户端 |
| requests | 2.31.0 | HTTP客户端 |
| gunicorn | 21.2.0 | WSGI服务器（生产环境） |

### 前端技术

| 技术 | 版本 | 说明 |
|------|------|------|
| Vue | 3.4+ | 渐进式框架 |
| Vue Router | 4.2+ | 路由管理 |
| Pinia | 2.1+ | 状态管理 |
| Element Plus | 2.5+ | UI组件库 |
| Axios | 1.6+ | HTTP客户端 |
| Vite | 5.0+ | 构建工具 |

### 部署技术

- **Docker**: 容器化
- **Docker Compose**: 服务编排
- **Nginx**: 前端静态资源服务和反向代理

---

## 📁 项目结构

```
dataMaker/
├── 📂 backend/                    # 后端Flask应用
│   ├── app.py                     # Flask主应用，注册API蓝图
│   ├── requirements.txt           # Python依赖清单
│   ├── Dockerfile                 # 后端Docker配置
│   └── api/                       # API蓝图目录
│       ├── __init__.py            # API包初始化
│       ├── appoint.py             # 课程预约API（添加/列表/状态变更/打星）
│       ├── redis.py               # Redis工具API（批量删除/查询）
│       ├── ai_teacher.py          # AI外教API（点数/兑换码/学习计划）
│       └── elf.py                 # 精灵系统API（等级/任务/排行榜/结课）
│
├── 📂 frontend/                   # 前端Vue应用
│   ├── package.json               # NPM依赖配置
│   ├── vite.config.js             # Vite构建配置
│   ├── Dockerfile                 # 前端Docker配置（多阶段构建）
│   ├── nginx.conf                 # Nginx配置（反向代理）
│   └── src/
│       ├── main.js                # Vue应用入口
│       ├── App.vue                # 根组件
│       ├── layout/                # 布局组件
│       │   └── MainLayout.vue     # 主布局（侧边栏+顶栏+标签页）
│       ├── router/                # 路由配置
│       │   └── index.js           # 路由定义（14个页面路由）
│       ├── stores/                # Pinia状态管理
│       │   └── tabs.js            # 标签页状态
│       ├── api/                   # API封装
│       │   ├── request.js         # Axios实例配置
│       │   ├── appoint.js         # 预约API封装
│       │   ├── redis.js           # Redis工具API封装
│       │   ├── aiTeacher.js       # AI外教API封装
│       │   └── elf.js             # 精灵API封装
│       └── views/                 # 页面组件
│           ├── Home.vue           # 首页（快捷入口）
│           ├── appoint/           # 预约管理页面
│           │   ├── AddAppoint.vue    # 添加预约（时间限制）
│           │   ├── AppointList.vue   # 预约列表（查询/状态变更）
│           │   └── AddStar.vue       # 预约打星
│           ├── redis/             # Redis工具页面
│           │   └── RedisTool.vue     # 批量删除工具
│           ├── aiTeacher/         # AI外教管理页面
│           │   ├── AddPoint.vue      # 添加点数
│           │   ├── ExchangeCode.vue  # 兑换码管理
│           │   └── ClearPlan.vue     # 清空学习计划
│           └── elf/               # 精灵系统页面
│               ├── ChangeLevel.vue   # 修改等级
│               ├── AddStar.vue       # 添加星星
│               ├── QueryTask.vue     # 查询任务
│               ├── DelTask.vue       # 删除任务
│               ├── EndClass.vue      # 精灵结课
│               └── ManageRank.vue    # 排行榜管理
│
├── 📂 common/                     # 公共工具模块（Python）
│   ├── db_connect.py              # 数据库连接和CRUD封装
│   ├── db_utils.py                # 配置文件读取工具
│   ├── api_client.py              # HTTP请求封装（GET/POST）
│   ├── delete_redis.py            # Redis批量删除工具类（核心）
│   ├── search_redis.py            # Redis查询工具
│   ├── execute_batch.py           # 批量数据库操作执行器
│   └── elf_level_config.py        # 精灵等级配置数据
│
├── 📂 config/                     # 配置文件目录
│   └── database.json              # 数据库连接配置
│
├── 📂 appoint/                    # 预约相关Python脚本
│   ├── add_appoint_cn.py          # 添加普通话预约
│   ├── add_appoint_en.py          # 添加英语预约
│   ├── change_appoint_status.py   # 修改预约状态
│   ├── appoint_add_star.py        # 预约打星
│   └── search_appoints.py         # 查询预约信息
│
├── 📂 elf/                        # 精灵系统Python脚本
│   ├── elf_change_level.py        # 修改精灵等级
│   ├── elf_add_star.py            # 精灵数据打星
│   ├── elf_create_task.py         # 创建精灵任务
│   ├── elf_del_task.py            # 删除精灵任务
│   ├── elf_rank.py                # 精灵排行榜管理
│   └── elf_create_endclass_java.py # 精灵结课
│
├── 📂 aiTeacher/                  # AI外教Python脚本
│   ├── ai_add_point.py            # 添加AI点数
│   ├── ai_add_exchange_code.py    # 添加兑换码
│   └── ai_del_studyplan_all.py    # 清空学习计划
│
├── 📂 orders/                     # 订单管理脚本
│   └── add_order.py               # 创建订单
│
├── 📂 picturebook/                # 绘本系统脚本
│   └── pb_del_data.py             # 删除绘本数据
│
├── 📂 tools/                      # 其他辅助工具
│   ├── del_redis.py               # Redis删除工具
│   ├── high_risk_user_device.py   # 高风险用户设备管理
│   └── url_unquote.py             # URL解码工具
│
├── docker-compose.yml             # Docker编排配置
├── .gitignore                     # Git忽略文件配置
├── CLAUDE.md                      # 项目上下文文档（AI开发参考）
├── IMPLEMENTATION_GUIDE.md        # 实施指南
├── README_WEB.md                  # Web平台使用文档
└── README.md                      # 本文档
```

---

## 🌐 页面路由

| 路由路径 | 页面名称 | 功能说明 |
|---------|---------|---------|
| `/` 或 `/home` | 首页 | 快捷入口和系统信息 |
| `/appoint/add` | 添加预约 | 创建课程预约（时间限制） |
| `/appoint/list` | 预约列表 | 查询和管理预约 |
| `/appoint/star` | 预约打星 | 课程评价 |
| `/redis/tool` | Redis工具 | 批量删除键 |
| `/ai/add-point` | 添加财富 | 添加AI点数 |
| `/ai/exchange-code` | 兑换码 | 兑换码管理 |
| `/ai/clear-plan` | 清空学习计划 | 重置AI学习进度 |
| `/elf/add-star` | 添加星星 | 精灵星星奖励 |
| `/elf/change-level` | 修改等级 | 精灵等级管理 |
| `/elf/end-class` | 精灵结课 | 批量结课操作 |
| `/elf/query-task` | 查询任务 | 查看精灵任务 |
| `/elf/del-task` | 删除任务 | 清空精灵任务 |
| `/elf/manage-rank` | 管理排行榜 | 重置排行榜 |

---

## 🔌 API接口文档

### 课程预约 API

#### POST `/api/appoint/add_cn`
添加普通话预约

**请求参数:**
```json
{
  "stu_id": "12345678",
  "t_id": "350012781",
  "start_time": "2026-01-16 09:00:00",
  "end_time": "2026-01-16 09:30:00",
  "date_time": "20260116_19",
  "course_type": "31",
  "use_point": "buy",
  "status": "on"
}
```

#### POST `/api/appoint/add_en`
添加英语预约

#### GET `/api/appoint/list`
查询预约列表

**请求参数:**
- `page`: 页码（默认1）
- `pageSize`: 每页数量（默认20）
- `stuId`: 学生ID（可选）
- `tId`: 教师ID（可选）
- `status`: 状态（可选）
- `courseType`: 课程类型（可选）
- `category`: 课程种类（可选）
- `startDate`: 开始日期（可选）
- `endDate`: 结束日期（可选）

#### POST `/api/appoint/update_status`
修改预约状态（调用外部接口）

**请求参数:**
```json
{
  "id": "577708964",
  "status": "end"
}
```

### Redis工具 API

#### POST `/api/redis/delete`
批量删除Redis键

**请求参数:**
```json
{
  "mode": "pattern",
  "pattern": "user:*",
  "dry_run": true,
  "batch_size": 100
}
```

### 精灵系统 API

#### POST `/api/elf/change_level`
修改精灵等级

#### POST `/api/elf/query_task`
查询精灵任务

#### POST `/api/elf/delete_task`
删除精灵任务

#### POST `/api/elf/manage_rank`
管理排行榜

### AI外教 API

#### POST `/api/ai/add_point`
添加AI点数

#### POST `/api/ai/add_exchange_code`
添加兑换码

#### POST `/api/ai/clear_plan`
清空学习计划

---

## 🐛 常见问题

### 1. Docker启动失败

**问题**: 端口被占用或网络问题

**解决方案**:
```bash
# 检查端口占用
netstat -ano | findstr "5001"
netstat -ano | findstr "8080"

# 修改docker-compose.yml端口映射
ports:
  - "5002:5001"  # 使用其他端口
  - "8081:80"
```

### 2. 前端无法访问后端API

**问题**: CORS跨域错误

**解决方案**:
- 确认后端已启动并运行在正确端口
- 检查 `backend/app.py` 中 CORS 配置
- 检查浏览器控制台具体错误信息

### 3. 时间选择器无法选择分钟

**问题**: 时间限制功能未生效

**解决方案**:
- 确认前端代码已更新（`AddAppoint.vue` 包含 `disabledMinutes` 函数）
- 刷新浏览器缓存（Ctrl+F5）
- 检查浏览器控制台是否有JavaScript错误

### 4. 预约状态变更失败

**问题**: 外部API调用失败

**解决方案**:
- 检查外部API地址是否可访问
- 查看后端日志: `docker-compose logs backend`
- 确认预约ID是否存在

### 5. 数据库连接失败

**问题**: 无法连接到MySQL数据库

**解决方案**:
- 检查 `config/database.json` 配置
- 确认数据库服务器可访问
- 测试数据库连接: `python common/db_connect.py`

---

## 🔄 开发指南

### 添加新功能页面

#### 1. 创建后端API

```python
# backend/api/new_module.py
from flask import Blueprint, request, jsonify

new_bp = Blueprint('new_module', __name__)

@new_bp.route('/action', methods=['POST'])
def action():
    data = request.json
    # 处理逻辑
    return jsonify({'code': '10000', 'message': '成功'})
```

注册蓝图（`backend/app.py`）:
```python
from api.new_module import new_bp
app.register_blueprint(new_bp, url_prefix='/api/new')
```

#### 2. 创建前端页面

```vue
<!-- frontend/src/views/new/NewPage.vue -->
<template>
  <div class="new-page">
    <el-card>
      <template #header>
        <span>新功能页面</span>
      </template>
      <!-- 页面内容 -->
    </el-card>
  </div>
</template>

<script setup>
// 页面逻辑
</script>
```

#### 3. 添加路由

```javascript
// frontend/src/router/index.js
{
  path: '/new/page',
  name: 'NewPage',
  component: () => import('@/views/new/NewPage.vue'),
  meta: { title: '新功能', icon: 'Plus' }
}
```

#### 4. 更新菜单

在 `MainLayout.vue` 中添加菜单项。

### 调试技巧

**后端调试:**
```bash
# 启用Flask调试模式
cd backend
export FLASK_ENV=development  # Windows: set FLASK_ENV=development
python app.py
```

**前端调试:**
```bash
# 使用Vue DevTools
cd frontend
npm run dev
# 浏览器打开开发者工具，查看Vue组件状态
```

**Docker调试:**
```bash
# 查看容器日志
docker-compose logs -f backend
docker-compose logs -f frontend

# 进入容器内部
docker-compose exec backend bash
docker-compose exec frontend sh
```

---

## 📝 更新日志

### v1.2.0 (2026-01-15) - 最新版本

**新增功能:**
- ✅ 添加预约时间选择器限制（仅整点和半点）
- ✅ 预约状态变更改为调用外部接口
- ✅ 完善Docker端口配置统一为5001
- ✅ 更新.gitignore添加node_modules规则

### v1.1.0 (2026-01-14)

**新增模块:**
- ✅ AI外教管理模块（3个功能页面）
- ✅ 精灵系统管理模块（6个功能页面）
- ✅ 预约列表查询和状态管理

**技术优化:**
- ✅ 后端API蓝图架构完善
- ✅ 前端路由和菜单系统完善
- ✅ Docker配置优化

### v1.0.0 (2026-01-09)

**首次发布:**
- ✅ 基础布局系统（侧边栏+顶栏+标签页）
- ✅ 首页快捷入口
- ✅ 添加预约功能
- ✅ Docker容器化部署
- ✅ Python脚本工具集

---

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

### 提交Issue

遇到问题请到 [GitHub Issues](https://github.com/caobaoling/data_maker/issues) 提交，包含以下信息：
- 问题描述
- 复现步骤
- 环境信息（操作系统、浏览器、Docker版本等）
- 错误日志或截图

### 提交Pull Request

1. Fork项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

---

## 📞 技术支持

### 相关文档

- 📚 [CLAUDE.md](CLAUDE.md) - 项目详细技术文档
- 📖 [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) - 实施指南
- 🌐 [README_WEB.md](README_WEB.md) - Web平台使用文档

### 技术资源

- [Vue 3 官方文档](https://cn.vuejs.org/)
- [Element Plus 组件库](https://element-plus.org/zh-CN/)
- [Flask 官方文档](https://flask.palletsprojects.com/)
- [Docker 官方文档](https://docs.docker.com/)

### 联系方式

- GitHub: [@caobaoling](https://github.com/caobaoling)
- 项目地址: https://github.com/caobaoling/data_maker

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

感谢以下开源项目：

- [Vue.js](https://vuejs.org/) - 渐进式JavaScript框架
- [Element Plus](https://element-plus.org/) - 基于Vue 3的组件库
- [Flask](https://flask.palletsprojects.com/) - Python Web框架
- [Docker](https://www.docker.com/) - 容器化平台

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给个Star吧！⭐**

Made with ❤️ by [DataMaker Team](https://github.com/caobaoling)

</div>

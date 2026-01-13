# DataMaker Web 管理平台 - 使用文档

## 📦 项目概述

DataMaker 是一个测试数据管理 Web 平台，用于快速操作教育平台的测试数据。

**技术栈:**
- 后端: Flask + Python 3.11
- 前端: Vue 3 + Element Plus + Vite
- 部署: Docker + Docker Compose

**主要功能:**
- ✅ 课程预约管理 (添加预约、预约列表、预约打星)
- 🔲 精灵系统管理 (开发中)
- 🔲 AI外教管理 (开发中)
- 🔲 Redis工具箱 (开发中)

---

## 🚀 快速开始

### 方式一: Docker部署 (推荐)

**前提条件:**
- Docker 20.10+
- Docker Compose 2.0+

**启动步骤:**

```bash
# 1. 进入项目目录
cd D:\dataMaker

# 2. 构建并启动服务
docker-compose up -d

# 3. 查看服务状态
docker-compose ps

# 4. 查看日志
docker-compose logs -f
```

**访问地址:**
- 前端: http://localhost:8080
- 后端API: http://localhost:5000

**停止服务:**
```bash
docker-compose down
```

---

### 方式二: 本地开发运行

#### 后端启动

```bash
# 1. 进入后端目录
cd backend

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动Flask服务
python app.py

# 运行在 http://localhost:5000
```

#### 前端启动

```bash
# 1. 进入前端目录
cd frontend

# 2. 安装依赖
npm install

# 3. 启动开发服务器
npm run dev

# 运行在 http://localhost:3000
```

---

## 📖 功能说明

### 1. 首页

- 快捷操作卡片: 点击快速进入对应功能
- 系统信息: 显示版本、环境、状态
- 使用说明: 基本操作提示

### 2. 添加预约

**支持功能:**
- 选择课程类型 (普通话/英语)
- 输入学生ID和教师ID (无验证)
- 选择开始时间 (自动计算结束时间)
- 选择课程性质 (付费课/体验课)
- 手动修改教材ID (提供默认值)
- 预览请求JSON

**操作步骤:**
1. 选择课程类型 (普通话或英语)
2. 填写学生ID (必填)
3. 填写教师ID (必填，仅数字)
4. 选择开始时间
5. 选择课程性质
6. 点击"创建预约"提交

**注意事项:**
- 教师ID需手动输入,不做格式验证
- 教材ID可使用默认值或手动修改
- 结束时间和date_time自动计算

### 3. 预约列表

当前为占位页面，后续将实现:
- 预约数据查询
- 状态筛选
- 批量操作
- 状态修改

### 4. 预约打星

当前为占位页面，预计第二期实现。

---

## 🎯 界面导航

### 顶部栏
- **左侧**: 折叠/展开按钮 + 系统标题
- **右侧**: 用户名下拉菜单 + 退出按钮

### 侧边菜单
- **课程预约**: 添加预约 | 预约列表 | 预约打星
- **精灵系统**: 开发中
- **AI外教**: 开发中
- **Redis工具**: 开发中

### 多标签页
- 标签可关闭 (首页除外)
- 点击标签切换页面
- 关闭标签返回上一个标签

---

## 🔧 配置说明

### 数据库配置

编辑 `config/database.json`:

```json
{
    "host": "172.16.70.20",
    "port": 3306,
    "user": "rd_user",
    "password": "NTHXDF7czYwi"
}
```

### API端点配置

后端默认使用以下API端点:

```python
# 课程预约API
APPOINT_API = "http://172.16.16.97/talkplatform_appointone_consumer/v1/appoint/add"
```

如需修改，编辑 `backend/api/appoint.py`。

---

## 📁 项目结构

```
dataMaker/
├── backend/                 # 后端Flask应用
│   ├── app.py              # 主应用
│   ├── api/                # API路由
│   │   └── appoint.py      # 预约API
│   ├── requirements.txt    # Python依赖
│   └── Dockerfile          # Docker配置
│
├── frontend/               # 前端Vue应用
│   ├── src/
│   │   ├── layout/         # 布局组件
│   │   │   └── MainLayout.vue
│   │   ├── views/          # 页面组件
│   │   │   ├── Home.vue
│   │   │   └── appoint/    # 预约相关页面
│   │   ├── router/         # 路由配置
│   │   ├── stores/         # 状态管理
│   │   └── api/            # API封装
│   ├── package.json
│   ├── vite.config.js
│   ├── Dockerfile
│   └── nginx.conf
│
├── common/                 # 公共模块(复用现有)
├── config/                 # 配置文件
├── docker-compose.yml      # Docker编排
└── README_WEB.md          # 本文档
```

---

## 🐛 常见问题

### 1. Docker构建失败

**问题**: 网络超时或依赖安装失败

**解决**:
```bash
# 使用国内镜像源
# Python: requirements.txt 使用清华源
# Node.js: package.json 使用淘宝源
```

### 2. 前端无法访问后端API

**问题**: CORS跨域错误

**解决**: 确认 `backend/app.py` 中 CORS 配置正确:
```python
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

### 3. 端口被占用

**问题**: 5000或8080端口已被占用

**解决**:
```bash
# 修改 docker-compose.yml 中的端口映射
ports:
  - "5001:5000"  # 后端改为5001
  - "8081:80"    # 前端改为8081
```

### 4. 页面空白无内容

**问题**: 前端路由或组件加载失败

**解决**:
1. 检查浏览器控制台错误
2. 确认所有组件文件已创建
3. 检查路由配置是否正确

---

## 🔄 开发指南

### 添加新功能

1. **后端API**: 在 `backend/api/` 目录创建新的蓝图
2. **前端页面**: 在 `frontend/src/views/` 创建新组件
3. **路由配置**: 更新 `frontend/src/router/index.js`
4. **菜单配置**: 更新 `MainLayout.vue` 中的菜单项

### 调试技巧

**后端调试:**
```bash
cd backend
# 启用Flask调试模式
export FLASK_ENV=development
python app.py
```

**前端调试:**
```bash
cd frontend
# Vue DevTools
# 浏览器控制台查看网络请求
npm run dev
```

### 构建生产版本

```bash
# 前端构建
cd frontend
npm run build

# 查看构建产物
ls dist/
```

---

## 📝 更新日志

### v1.0.0 (2026-01-09)

**新增功能:**
- ✅ 基础布局系统 (可折叠侧边菜单 + 多标签页)
- ✅ 首页快捷入口
- ✅ 添加预约功能 (简化版，无验证)
- ✅ 预约列表占位
- ✅ 预约打星占位
- ✅ Docker容器化部署

**技术特性:**
- Vue 3 + Element Plus
- Flask + CORS
- Docker + Docker Compose
- Nginx反向代理

---

## 📞 技术支持

**项目文档:**
- 实施指南: `IMPLEMENTATION_GUIDE.md`
- CLAUDE文档: `CLAUDE.md`

**遇到问题:**
1. 查看日志: `docker-compose logs -f`
2. 检查网络: `docker-compose ps`
3. 重启服务: `docker-compose restart`

**下一步计划:**
- [ ] 实现预约列表查询功能
- [ ] 实现预约打星功能
- [ ] 添加精灵系统管理
- [ ] 添加Redis工具箱
- [ ] 完善权限控制

---

## 🎉 开始使用

现在您可以:

1. **Docker部署**: `docker-compose up -d`
2. **访问平台**: http://localhost:8080
3. **开始测试**: 点击"添加预约"创建测试数据

祝使用愉快！🚀

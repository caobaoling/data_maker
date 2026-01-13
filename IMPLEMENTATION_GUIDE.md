# DataMaker Web 管理平台 - 完整实施文档

## 📦 项目已创建文件清单

### 后端文件 (已完成)
```
backend/
├── app.py                    # Flask主应用 ✅
├── requirements.txt          # Python依赖 ✅
├── Dockerfile               # Docker配置 ✅
└── api/
    ├── __init__.py          # API包初始化 ✅
    └── appoint.py           # 预约API ✅
```

### 前端基础文件 (已完成)
```
frontend/
├── package.json             # NPM配置 ✅
├── vite.config.js          # Vite配置 ✅
├── index.html              # HTML入口 ✅
└── src/
    ├── main.js             # Vue入口 ✅
    ├── App.vue             # 根组件 ✅
    ├── router/index.js     # 路由配置 ✅
    ├── stores/tabs.js      # 标签页状态管理 ✅
    └── api/
        ├── request.js      # Axios封装 ✅
        └── appoint.js      # 预约API ✅
```

## 🎯 待创建的关键文件

### 1. 布局系统组件 (核心)

**MainLayout.vue** - 主布局框架
- 顶部栏 + 侧边菜单 + 多标签页 + 内容区域
- 折叠/展开状态管理
- keep-alive缓存

**Header.vue** - 精简顶部栏
- 仅保留: 折叠按钮 + 标题 + 用户名下拉 + 退出按钮

**SideMenu.vue** - 侧边手风琴菜单
- Element Plus el-menu 实现
- 手风琴效果 (unique-opened)
- 折叠模式 (64px宽,仅图标)

**TabsView.vue** - 多标签页组件
- 标签可关闭/拖拽
- 右键菜单
- 状态持久化

### 2. 页面组件

**views/Home.vue** - 首页
- 快捷入口卡片
- 系统信息面板
- 使用说明

**views/appoint/AddAppoint.vue** - 添加预约(简化版)
- 无验证规则
- 教师ID手动输入
- 教材默认值
- 预览JSON功能

**views/appoint/AppointList.vue** - 预约列表
- 查询工具栏
- 数据表格
- 状态修改对话框

**views/appoint/AddStar.vue** - 预约打星占位
- 显示开发中提示
- 功能说明
- 返回按钮

## 🚀 快速启动指南

### 1. 安装依赖

**后端:**
```bash
cd backend
pip install -r requirements.txt
```

**前端:**
```bash
cd frontend
npm install
```

### 2. 启动开发服务

**后端 (Flask):**
```bash
cd backend
python app.py
# 运行在 http://localhost:5000
```

**前端 (Vite):**
```bash
cd frontend
npm run dev
# 运行在 http://localhost:3000
```

### 3. 访问应用

打开浏览器访问: http://localhost:3000

## 🐳 Docker 部署

### docker-compose.yml (待创建)
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    volumes:
      - ./common:/app/common
      - ./config:/app/config
    environment:
      - FLASK_ENV=production

  frontend:
    build: ./frontend
    ports:
      - "8080:80"
    depends_on:
      - backend
```

### 一键启动
```bash
docker-compose up -d
```

访问: http://localhost:8080

## 📝 完整组件代码示例

### MainLayout.vue (简化版示例)
```vue
<template>
  <el-container class="main-layout">
    <el-header height="60px">
      <Header @toggle-sidebar="toggleSidebar" />
    </el-header>

    <el-container>
      <el-aside :width="sidebarWidth">
        <SideMenu :collapse="isCollapse" />
      </el-aside>

      <el-container>
        <div class="tabs-bar">
          <TabsView />
        </div>

        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import Header from './Header.vue'
import SideMenu from './SideMenu.vue'
import TabsView from './TabsView.vue'

const isCollapse = ref(false)
const sidebarWidth = computed(() => isCollapse.value ? '64px' : '200px')

const toggleSidebar = () => {
  isCollapse.value = !isCollapse.value
}
</script>
```

## 🎨 Element Plus 使用说明

### 主要组件
- **el-container**: 布局容器
- **el-menu**: 侧边菜单(支持手风琴)
- **el-form**: 表单组件
- **el-table**: 数据表格
- **el-card**: 卡片容器
- **el-dialog**: 对话框
- **el-button**: 按钮
- **el-icon**: 图标

### 安装图标库
已在 main.js 中全局注册所有图标:
```javascript
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
```

使用方式:
```vue
<el-icon><Calendar /></el-icon>
```

## 📚 开发建议

### 1. 组件开发顺序
1. ✅ 先完成布局系统(MainLayout/Header/SideMenu/TabsView)
2. ✅ 再开发首页(快捷入口)
3. ✅ 然后开发添加预约页面
4. ✅ 最后完善预约列表和占位页面

### 2. 样式规范
- 使用 Element Plus 默认主题色
- 间距统一: 8px的倍数(8/16/24/32)
- 卡片圆角: 4px
- 阴影使用 Element Plus 内置

### 3. 状态管理
- 标签页状态: stores/tabs.js
- 其他全局状态按需添加

### 4. API调用
- 统一使用 api/ 目录下的封装
- 错误处理在 request.js 拦截器中统一处理

## ⚠️ 重要提示

1. **前端开发模式**: 使用 Vite 代理转发 /api 请求到后端
2. **生产模式**: 使用 Nginx 反向代理
3. **环境变量**: 后续可添加 .env 文件配置不同环境
4. **权限控制**: 当前未实现登录,仅用户名下拉菜单占位

## 🔄 下一步工作

1. [ ] 创建完整的布局组件
2. [ ] 实现所有页面组件
3. [ ] 添加 Nginx 配置
4. [ ] 完善 Docker 配置
5. [ ] 编写详细使用文档

## 📞 技术支持

遇到问题请参考:
- Vue 3 文档: https://cn.vuejs.org/
- Element Plus 文档: https://element-plus.org/zh-CN/
- Flask 文档: https://flask.palletsprojects.com/

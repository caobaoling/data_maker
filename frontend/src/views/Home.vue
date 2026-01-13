<template>
  <div class="home-page">
    <h1 class="welcome-title">欢迎使用 DataMaker 测试数据管理平台</h1>

    <!-- 快捷操作卡片 -->
    <div class="section">
      <h2 class="section-title">🎯 快捷操作菜单</h2>
      <div class="module-cards">
        <el-card class="module-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span class="module-icon">📚</span>
              <span class="module-title">课程预约</span>
            </div>
          </template>
          <div class="card-body">
            <el-button text @click="navigateTo('/appoint/add', '添加预约')">
              ➕ 添加预约
            </el-button>
            <el-button text @click="navigateTo('/appoint/list', '预约列表')">
              📋 预约列表
            </el-button>
            <el-button text @click="navigateTo('/appoint/star', '预约打星')">
              ⭐ 预约打星
            </el-button>
          </div>
        </el-card>

        <el-card class="module-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span class="module-icon">🧚</span>
              <span class="module-title">精灵系统</span>
            </div>
          </template>
          <div class="card-body">
            <el-button text disabled>🔧 等级管理 (开发中)</el-button>
            <el-button text disabled>📊 任务管理 (开发中)</el-button>
            <el-button text disabled>🏆 排行榜 (开发中)</el-button>
          </div>
        </el-card>

        <el-card class="module-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span class="module-icon">🤖</span>
              <span class="module-title">AI外教</span>
            </div>
          </template>
          <div class="card-body">
            <el-button text disabled>💰 点数管理 (开发中)</el-button>
            <el-button text disabled>🎫 兑换码 (开发中)</el-button>
            <el-button text disabled>📖 学习计划 (开发中)</el-button>
          </div>
        </el-card>

        <el-card class="module-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span class="module-icon">🗄️</span>
              <span class="module-title">Redis工具</span>
            </div>
          </template>
          <div class="card-body">
            <el-button text disabled>🔍 搜索键 (开发中)</el-button>
            <el-button text disabled>🗑️ 批量删除 (开发中)</el-button>
            <el-button text disabled>👁️ 查看值 (开发中)</el-button>
          </div>
        </el-card>
      </div>
    </div>

    <!-- 系统信息 -->
    <div class="section">
      <h2 class="section-title">系统信息</h2>
      <el-card>
        <el-descriptions :column="3" border>
          <el-descriptions-item label="⚙️ 系统版本">v1.0.0</el-descriptions-item>
          <el-descriptions-item label="🌐 当前环境">测试环境</el-descriptions-item>
          <el-descriptions-item label="📡 后端状态">
            <el-tag type="success" size="small">● 正常</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="💾 数据库">
            <el-tag type="success" size="small">● 已连接</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="📅 当前时间" :span="2">
            {{ currentTime }}
          </el-descriptions-item>
        </el-descriptions>
      </el-card>
    </div>

    <!-- 使用说明 -->
    <div class="section">
      <h2 class="section-title">使用说明</h2>
      <el-card>
        <el-alert title="💡 提示" type="info" :closable="false" show-icon>
          <ul class="tips-list">
            <li>点击上方卡片快速进入对应功能模块</li>
            <li>左侧菜单可折叠展开以节省空间</li>
            <li>多标签页支持同时操作多个功能</li>
            <li>标签页可拖拽排序，右键有更多操作</li>
          </ul>
        </el-alert>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTabsStore } from '@/stores/tabs'

const router = useRouter()
const tabsStore = useTabsStore()
const currentTime = ref('')

const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString('zh-CN', { hour12: false })
}

let timer = null
onMounted(() => {
  updateTime()
  timer = setInterval(updateTime, 1000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})

const navigateTo = (path, title) => {
  router.push(path)
  tabsStore.addTab({ path, title })
}
</script>

<style scoped>
.home-page {
  padding: 24px;
}

.welcome-title {
  text-align: center;
  font-size: 28px;
  margin-bottom: 30px;
}

.section {
  margin-bottom: 30px;
}

.section-title {
  font-size: 20px;
  margin-bottom: 16px;
  padding-left: 10px;
  border-left: 4px solid #409eff;
}

.module-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.module-card {
  transition: all 0.3s;
}

.module-card:hover {
  transform: translateY(-5px);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
}

.module-icon {
  font-size: 24px;
}

.module-title {
  font-size: 16px;
  font-weight: 500;
}

.card-body {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 10px;
}

.tips-list {
  margin: 10px 0 0 20px;
  list-style: disc;
}

.tips-list li {
  margin-bottom: 8px;
  line-height: 1.6;
}
</style>

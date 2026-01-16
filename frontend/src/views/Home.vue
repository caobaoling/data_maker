<template>
  <div class="home-page">
    <h1 class="welcome-title">欢迎使用 DataMaker 测试数据管理平台</h1>

    <!-- 快捷操作卡片 -->
    <div class="section">
      <h2 class="section-title">🎯 快捷操作菜单</h2>
      <div class="module-cards">
        <!-- 课程预约模块 -->
        <el-card class="module-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span class="module-icon">📚</span>
              <span class="module-title">课程预约</span>
            </div>
          </template>
          <div class="card-body">
            <el-button type="primary" text @click="navigateTo('/appoint/add', '添加预约')">
              ➕ 添加预约
            </el-button>
            <el-button type="primary" text @click="navigateTo('/appoint/list', '预约列表')">
              📋 预约列表
            </el-button>
            <!-- 预约打星功能暂时隐藏 -->
            <!-- <el-button type="primary" text @click="navigateTo('/appoint/star', '预约打星')">
              ⭐ 预约打星
            </el-button> -->
          </div>
        </el-card>

        <!-- 精灵系统模块 -->
        <el-card class="module-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span class="module-icon">🧚</span>
              <span class="module-title">精灵系统</span>
            </div>
          </template>
          <div class="card-body">
            <el-button type="primary" text @click="navigateTo('/elf/add-star', '添加星星')">
              ⭐ 添加星星
            </el-button>
            <el-button type="primary" text @click="navigateTo('/elf/change-level', '修改等级')">
              🏆 修改等级
            </el-button>
            <el-button type="primary" text @click="navigateTo('/elf/del-task', '删除任务')">
              🗑️ 删除任务
            </el-button>
            <el-button type="primary" text @click="navigateTo('/elf/manage-rank', '管理排行榜')">
              📊 管理排行榜
            </el-button>
          </div>
        </el-card>

        <!-- AI外教模块 -->
        <el-card class="module-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span class="module-icon">🤖</span>
              <span class="module-title">AI外教</span>
            </div>
          </template>
          <div class="card-body">
            <el-button type="primary" text @click="navigateTo('/ai/add-point', '添加财富')">
              💰 添加财富
            </el-button>
            <el-button type="primary" text @click="navigateTo('/ai/exchange-code', '兑换码')">
              🎫 兑换码
            </el-button>
            <el-button type="primary" text @click="navigateTo('/ai/clear-plan', '清空学习计划')">
              🗑️ 清空学习计划
            </el-button>
          </div>
        </el-card>

        <!-- Redis工具模块 -->
        <el-card class="module-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span class="module-icon">🗄️</span>
              <span class="module-title">Redis工具</span>
            </div>
          </template>
          <div class="card-body">
            <el-button type="primary" text @click="navigateTo('/redis/tool', 'Redis工具')">
              🔧 Redis批量操作
            </el-button>
            <p class="feature-desc">支持按模式/前缀/后缀批量删除键</p>
          </div>
        </el-card>

        <!-- 绘本系统模块 -->
        <el-card class="module-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span class="module-icon">📖</span>
              <span class="module-title">绘本</span>
            </div>
          </template>
          <div class="card-body">
            <el-button type="primary" text @click="navigateTo('/picturebook/clear-plan', '清除绘本学习计划')">
              🗑️ 清除学习计划
            </el-button>
            <p class="feature-desc">清除用户绘本数据和Redis缓存</p>
          </div>
        </el-card>
      </div>
    </div>

    <!-- 系统信息 -->
    <div class="section">
      <h2 class="section-title">📊 系统信息</h2>
      <el-card>
        <el-descriptions :column="3" border>
          <el-descriptions-item label="⚙️ 系统版本">v1.2.0</el-descriptions-item>
          <el-descriptions-item label="🌐 当前环境">测试环境</el-descriptions-item>
          <el-descriptions-item label="📡 后端状态">
            <el-tag type="success" size="small">● 正常运行</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="💾 数据库">
            <el-tag type="success" size="small">● 已连接</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="🔧 Docker">
            <el-tag type="success" size="small">● 运行中</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="📅 当前时间">
            {{ currentTime }}
          </el-descriptions-item>
        </el-descriptions>
      </el-card>
    </div>

    <!-- 功能统计 -->
    <div class="section">
      <h2 class="section-title">✨ 功能统计</h2>
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-content">
              <div class="stat-icon" style="color: #409eff;">📚</div>
              <div class="stat-info">
                <div class="stat-label">课程预约</div>
                <div class="stat-value">2 个功能</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-content">
              <div class="stat-icon" style="color: #67c23a;">🧚</div>
              <div class="stat-info">
                <div class="stat-label">精灵系统</div>
                <div class="stat-value">4 个功能</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-content">
              <div class="stat-icon" style="color: #e6a23c;">🤖</div>
              <div class="stat-info">
                <div class="stat-label">AI外教</div>
                <div class="stat-value">3 个功能</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-content">
              <div class="stat-icon" style="color: #f56c6c;">🗄️</div>
              <div class="stat-info">
                <div class="stat-label">Redis工具</div>
                <div class="stat-value">1 个功能</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-content">
              <div class="stat-icon" style="color: #909399;">📖</div>
              <div class="stat-info">
                <div class="stat-label">绘本系统</div>
                <div class="stat-value">1 个功能</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 使用说明 -->
    <div class="section">
      <h2 class="section-title">💡 使用说明</h2>
      <el-card>
        <el-alert title="快速上手指南" type="info" :closable="false" show-icon>
          <ul class="tips-list">
            <li><strong>快捷访问：</strong>点击上方卡片快速进入对应功能模块</li>
            <li><strong>菜单导航：</strong>左侧菜单可折叠展开，支持搜索和快速定位</li>
            <li><strong>多标签页：</strong>支持同时打开多个页面，标签页可拖拽排序</li>
            <li><strong>预约管理：</strong>支持普通话和英语课程预约，时间自动限制为整点/半点</li>
            <li><strong>精灵系统：</strong>等级管理、任务删除、排行榜重置等完整功能</li>
            <li><strong>批量操作：</strong>Redis工具支持按模式批量删除，安全可靠</li>
          </ul>
        </el-alert>

        <el-divider />

        <el-alert title="⚠️ 注意事项" type="warning" :closable="false" show-icon style="margin-top: 16px;">
          <ul class="tips-list">
            <li>所有操作直接作用于测试环境数据库</li>
            <li>删除类操作不可恢复，请谨慎操作</li>
            <li>建议使用真实有效的学生ID和教师ID进行测试</li>
            <li>预约时间选择仅限整点（:00）或半点（:30）</li>
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

.feature-desc {
  margin-top: 8px;
  font-size: 12px;
  color: #909399;
  line-height: 1.5;
}

.stat-card {
  cursor: pointer;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  font-size: 36px;
}

.stat-info {
  flex: 1;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
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

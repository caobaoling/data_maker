<template>
  <el-container class="main-layout">
    <!-- 精简顶部栏 -->
    <el-header height="60px" class="main-header">
      <div class="header-left">
        <el-button :icon="Expand" circle @click="toggleSidebar" />
        <span class="title">DataMaker 测试数据管理平台</span>
      </div>
      <div class="header-right">
        <el-dropdown @command="handleCommand">
          <span class="user-dropdown">
            Admin <el-icon><arrow-down /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="logout" icon="SwitchButton">
                退出登录
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        <el-button type="danger" text @click="handleLogout">退出</el-button>
      </div>
    </el-header>

    <el-container>
      <!-- 侧边菜单 - 暗色主题 -->
      <el-aside :width="sidebarWidth" class="main-sidebar">
        <el-menu
          :default-active="activeMenu"
          :collapse="isCollapse"
          :unique-opened="true"
          background-color="#1f2d3d"
          text-color="#bfcbd9"
          active-text-color="#409eff"
          class="side-menu">

          <el-sub-menu index="appoint">
            <template #title>
              <el-icon><Calendar /></el-icon>
              <span>课程预约</span>
            </template>
            <el-menu-item index="/appoint/add" @click="handleMenuClick('/appoint/add', '添加预约')">
              添加预约
            </el-menu-item>
            <el-menu-item index="/appoint/list" @click="handleMenuClick('/appoint/list', '预约列表')">
              预约列表
            </el-menu-item>
            <el-menu-item index="/appoint/star" @click="handleMenuClick('/appoint/star', '预约打星')">
              预约打星
            </el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="elf" disabled>
            <template #title>
              <el-icon><Grid /></el-icon>
              <span>精灵系统</span>
            </template>
          </el-sub-menu>

          <el-sub-menu index="ai" disabled>
            <template #title>
              <el-icon><User /></el-icon>
              <span>AI外教</span>
            </template>
          </el-sub-menu>

          <el-sub-menu index="redis" disabled>
            <template #title>
              <el-icon><Coin /></el-icon>
              <span>Redis工具</span>
            </template>
          </el-sub-menu>
        </el-menu>
      </el-aside>

      <el-container class="main-content-wrapper">
        <!-- 多标签页 -->
        <div class="tabs-bar">
          <div class="tabs-wrapper">
            <div
              v-for="tab in visitedTabs"
              :key="tab.path"
              class="tab-item"
              :class="{ 'is-active': isActive(tab) }"
              @click="handleTabClick(tab)">
              <span>{{ tab.title }}</span>
              <el-icon v-if="!tab.affix" class="tab-close" @click.stop="handleTabClose(tab)">
                <Close />
              </el-icon>
            </div>
          </div>
        </div>

        <!-- 主内容区 -->
        <el-main class="main-content">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useTabsStore } from '@/stores/tabs'
import { ElMessageBox } from 'element-plus'
import { Expand, ArrowDown, Calendar, Grid, User, Coin, Close } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const tabsStore = useTabsStore()

const isCollapse = ref(false)
const activeMenu = ref('/home')
const sidebarWidth = computed(() => isCollapse.value ? '64px' : '200px')
const visitedTabs = computed(() => tabsStore.visitedTabs)

const toggleSidebar = () => {
  isCollapse.value = !isCollapse.value
}

const handleMenuClick = (path, title) => {
  router.push(path)
  tabsStore.addTab({ path, title })
  activeMenu.value = path
}

const isActive = (tab) => {
  return tab.path === route.path
}

const handleTabClick = (tab) => {
  router.push(tab.path)
}

const handleTabClose = (tab) => {
  tabsStore.closeTab(tab)
  if (isActive(tab)) {
    const lastTab = visitedTabs.value[visitedTabs.value.length - 1]
    router.push(lastTab.path)
  }
}

const handleCommand = (command) => {
  if (command === 'logout') {
    handleLogout()
  }
}

const handleLogout = () => {
  ElMessageBox.confirm('确定要退出系统吗？', '退出确认', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    localStorage.clear()
    window.location.reload()
  }).catch(() => {})
}
</script>

<style scoped>
.main-layout {
  height: 100vh;
}

.main-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  z-index: 10;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.title {
  font-size: 18px;
  font-weight: 500;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-dropdown {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 5px 10px;
}

/* 侧边栏暗色主题 */
.main-sidebar {
  background: #1f2d3d;
  overflow-x: hidden;
  transition: width 0.3s;
}

.side-menu {
  border: none;
  background: #1f2d3d;
  height: 100%;
}

/* 修复：让子菜单也是暗色 */
.side-menu :deep(.el-sub-menu__title) {
  background-color: #1f2d3d !important;
  color: #bfcbd9;
}

.side-menu :deep(.el-sub-menu__title:hover) {
  background-color: #263445 !important;
}

.side-menu :deep(.el-menu-item) {
  background-color: #1c2b36 !important;
  color: #bfcbd9;
}

.side-menu :deep(.el-menu-item:hover) {
  background-color: #263445 !important;
}

.side-menu :deep(.el-menu-item.is-active) {
  background-color: #409eff !important;
  color: #fff !important;
}

/* 确保折叠状态下也是暗色 */
.side-menu.el-menu--collapse :deep(.el-sub-menu__title) {
  background-color: #1f2d3d !important;
}

/* 主内容区包装器 - 确保标签栏在顶部不分割 */
.main-content-wrapper {
  display: flex;
  flex-direction: column;
  background: #fff;
}

/* 标签栏 - 紧贴主内容区顶部 */
.tabs-bar {
  height: 40px;
  background: #fff;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  padding: 0 10px;
  flex-shrink: 0;
}

.tabs-wrapper {
  display: flex;
  gap: 5px;
}

.tab-item {
  display: flex;
  align-items: center;
  padding: 0 12px;
  height: 32px;
  border: 1px solid #e4e7ed;
  border-radius: 3px;
  background: #fff;
  cursor: pointer;
  transition: all 0.3s;
}

.tab-item:hover {
  background: #f5f7fa;
}

.tab-item.is-active {
  background: #409eff;
  color: #fff;
  border-color: #409eff;
}

.tab-close {
  margin-left: 8px;
  font-size: 12px;
}

.tab-close:hover {
  color: #f56c6c;
}

/* 主内容区 */
.main-content {
  background: #f5f7fa;
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}
</style>

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
            <!-- 暂时隐藏：功能需要优化 -->
            <!-- <el-menu-item index="/appoint/star" @click="handleMenuClick('/appoint/star', '预约打星')">
              预约打星
            </el-menu-item> -->
          </el-sub-menu>

          <el-sub-menu index="elf">
            <template #title>
              <el-icon><Grid /></el-icon>
              <span>精灵系统</span>
            </template>
            <el-menu-item index="/elf/add-star" @click="handleMenuClick('/elf/add-star', '添加星星')">
              添加星星
            </el-menu-item>
            <el-menu-item index="/elf/change-level" @click="handleMenuClick('/elf/change-level', '修改等级')">
              修改等级
            </el-menu-item>
            <!-- 暂时隐藏：精灵结课功能 -->
            <!-- <el-menu-item index="/elf/end-class" @click="handleMenuClick('/elf/end-class', '精灵结课')">
              精灵结课
            </el-menu-item> -->
            <!-- 暂时隐藏：查询任务接口有问题 -->
            <!-- <el-menu-item index="/elf/query-task" @click="handleMenuClick('/elf/query-task', '查询任务')">
              查询任务
            </el-menu-item> -->
            <el-menu-item index="/elf/del-task" @click="handleMenuClick('/elf/del-task', '删除任务')">
              删除任务
            </el-menu-item>
            <el-menu-item index="/elf/manage-rank" @click="handleMenuClick('/elf/manage-rank', '管理排行榜')">
              管理排行榜
            </el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="ai">
            <template #title>
              <el-icon><User /></el-icon>
              <span>AI外教</span>
            </template>
            <el-menu-item index="/ai/exchange-code" @click="handleMenuClick('/ai/exchange-code', '兑换码')">
              兑换码
            </el-menu-item>
            <el-menu-item index="/ai/clear-plan" @click="handleMenuClick('/ai/clear-plan', '清空学习计划')">
              清空学习计划
            </el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="redis">
            <template #title>
              <el-icon><Coin /></el-icon>
              <span>Redis工具</span>
            </template>
            <el-menu-item index="/redis/tool" @click="handleMenuClick('/redis/tool', 'Redis工具')">
              Redis管理
            </el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="picturebook">
            <template #title>
              <el-icon><Reading /></el-icon>
              <span>绘本</span>
            </template>
            <el-menu-item index="/picturebook/clear-plan" @click="handleMenuClick('/picturebook/clear-plan', '清除绘本学习计划')">
              清除学习计划
            </el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="teacher">
            <template #title>
              <el-icon><UserFilled /></el-icon>
              <span>外教管理</span>
            </template>
            <el-menu-item index="/teacher/contract" @click="handleMenuClick('/teacher/contract', '给老师签合同(SA)')">
              给老师签合同(SA)
            </el-menu-item>
            <el-menu-item index="/teacher/email" @click="handleMenuClick('/teacher/email', '查看老师邮箱')">
              查看老师邮箱
            </el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="user">
            <template #title>
              <el-icon><User /></el-icon>
              <span>用户管理</span>
            </template>
            <el-menu-item index="/user/add-wealth" @click="handleMenuClick('/user/add-wealth', '添加财富')">
              添加财富
            </el-menu-item>
            <el-menu-item index="/user/arabic-student" @click="handleMenuClick('/user/arabic-student', '阿语学员')">
              阿语学员
            </el-menu-item>
            <el-menu-item index="/user/order" @click="handleMenuClick('/user/order', '订单管理')">
              订单管理
            </el-menu-item>
            <el-menu-item index="/user/release-risk" @click="handleMenuClick('/user/release-risk', '解除高风险')">
              解除高风险
            </el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="tools">
            <template #title>
              <el-icon><Tools /></el-icon>
              <span>其他功能</span>
            </template>
            <el-menu-item index="/tools/wordcloud" @click="handleMenuClick('/tools/wordcloud', '词云生成')">
              词云生成
            </el-menu-item>
            <el-menu-item index="/tools/number-formatter" @click="handleMenuClick('/tools/number-formatter', '数字格式化')">
              数字格式化
            </el-menu-item>
            <el-menu-item index="/tools/url-unquote" @click="handleMenuClick('/tools/url-unquote', '转义URL')">
              转义URL
            </el-menu-item>
          </el-sub-menu>
        </el-menu>
      </el-aside>

      <el-container class="main-content-wrapper">
        <!-- 多标签页 -->
        <div class="tabs-bar">
          <el-icon
            class="tab-nav-btn left"
            :class="{ 'is-disabled': scrollLeft <= 0 }"
            @click="scrollTabsLeft">
            <ArrowLeft />
          </el-icon>

          <div class="tabs-container" ref="tabsContainerRef">
            <div class="tabs-wrapper" ref="tabsWrapperRef">
              <div
                v-for="tab in visitedTabs"
                :key="tab.path"
                class="tab-item"
                :class="{ 'is-active': isActive(tab) }"
                @click="handleTabClick(tab)">
                <span class="tab-title">{{ tab.title }}</span>
                <el-icon v-if="!tab.affix" class="tab-close" @click.stop="handleTabClose(tab)">
                  <Close />
                </el-icon>
              </div>
            </div>
          </div>

          <el-icon
            class="tab-nav-btn right"
            :class="{ 'is-disabled': scrollLeft >= maxScrollLeft }"
            @click="scrollTabsRight">
            <ArrowRight />
          </el-icon>
        </div>

        <!-- 主内容区 -->
        <el-main class="main-content">
          <router-view v-slot="{ Component }">
            <keep-alive>
              <component :is="Component" />
            </keep-alive>
          </router-view>
        </el-main>
      </el-container>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useTabsStore } from '@/stores/tabs'
import { ElMessageBox } from 'element-plus'
import { Expand, ArrowDown, Calendar, Grid, User, Coin, Close, Reading, ArrowLeft, ArrowRight, UserFilled, Tools } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const tabsStore = useTabsStore()

const isCollapse = ref(false)
const activeMenu = ref(route.path)
const sidebarWidth = computed(() => isCollapse.value ? '64px' : '200px')
const visitedTabs = computed(() => tabsStore.visitedTabs)

// 标签栏滚动相关
const tabsContainerRef = ref(null)
const tabsWrapperRef = ref(null)
const scrollLeft = ref(0)
const maxScrollLeft = ref(0)

// 更新滚动状态
const updateScrollState = () => {
  if (tabsContainerRef.value && tabsWrapperRef.value) {
    scrollLeft.value = tabsContainerRef.value.scrollLeft
    maxScrollLeft.value = tabsWrapperRef.value.scrollWidth - tabsContainerRef.value.clientWidth
  }
}

// 向左滚动
const scrollTabsLeft = () => {
  if (tabsContainerRef.value) {
    const scrollAmount = 200
    tabsContainerRef.value.scrollTo({
      left: Math.max(0, tabsContainerRef.value.scrollLeft - scrollAmount),
      behavior: 'smooth'
    })
  }
}

// 向右滚动
const scrollTabsRight = () => {
  if (tabsContainerRef.value && tabsWrapperRef.value) {
    const scrollAmount = 200
    const maxScroll = tabsWrapperRef.value.scrollWidth - tabsContainerRef.value.clientWidth
    tabsContainerRef.value.scrollTo({
      left: Math.min(maxScroll, tabsContainerRef.value.scrollLeft + scrollAmount),
      behavior: 'smooth'
    })
  }
}

// 监听滚动事件
onMounted(() => {
  if (tabsContainerRef.value) {
    tabsContainerRef.value.addEventListener('scroll', updateScrollState)
    // 初始化滚动状态
    nextTick(updateScrollState)
  }
})

// 监听标签变化,更新滚动状态并自动滚动到最右侧
watch(visitedTabs, (newTabs, oldTabs) => {
  nextTick(() => {
    updateScrollState()

    // 如果标签数量增加了(新打开了标签),自动滚动到最右侧
    if (newTabs.length > oldTabs?.length) {
      scrollToRight()
    }
  })
}, { deep: true })

// 监听当前路由变化,切换到对应标签时自动滚动使其可见
watch(() => route.path, () => {
  nextTick(() => {
    scrollToActiveTab()
  })
})

// 滚动到最右侧
const scrollToRight = () => {
  if (tabsContainerRef.value && tabsWrapperRef.value) {
    const maxScroll = tabsWrapperRef.value.scrollWidth - tabsContainerRef.value.clientWidth
    tabsContainerRef.value.scrollTo({
      left: maxScroll,
      behavior: 'smooth'
    })
  }
}

// 滚动到激活的标签,确保其可见
const scrollToActiveTab = () => {
  if (!tabsContainerRef.value || !tabsWrapperRef.value) return

  const activeTabIndex = visitedTabs.value.findIndex(tab => tab.path === route.path)
  if (activeTabIndex === -1) return

  const tabItems = tabsWrapperRef.value.querySelectorAll('.tab-item')
  const activeTabElement = tabItems[activeTabIndex]

  if (activeTabElement) {
    const containerWidth = tabsContainerRef.value.clientWidth
    const scrollLeft = tabsContainerRef.value.scrollLeft
    const tabLeft = activeTabElement.offsetLeft
    const tabWidth = activeTabElement.offsetWidth

    // 如果标签在可视区域左侧外,滚动使其在左边缘可见
    if (tabLeft < scrollLeft) {
      tabsContainerRef.value.scrollTo({
        left: tabLeft,
        behavior: 'smooth'
      })
    }
    // 如果标签在可视区域右侧外,滚动使其在右边缘可见
    else if (tabLeft + tabWidth > scrollLeft + containerWidth) {
      tabsContainerRef.value.scrollTo({
        left: tabLeft + tabWidth - containerWidth,
        behavior: 'smooth'
      })
    }
  }
}

// 监听路由变化，自动同步菜单高亮
watch(() => route.path, (newPath) => {
  activeMenu.value = newPath
}, { immediate: true })

const toggleSidebar = () => {
  isCollapse.value = !isCollapse.value
}

const handleMenuClick = (path, title) => {
  router.push(path)
  tabsStore.addTab({ path, title })
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
  padding: 0 5px;
  flex-shrink: 0;
  position: relative;
}

/* 滚动按钮 */
.tab-nav-btn {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #606266;
  transition: all 0.3s;
  border-radius: 4px;
  font-size: 16px;
}

.tab-nav-btn:hover:not(.is-disabled) {
  background: #f5f7fa;
  color: #409eff;
}

.tab-nav-btn.is-disabled {
  color: #c0c4cc;
  cursor: not-allowed;
  opacity: 0.5;
}

.tab-nav-btn.left {
  margin-right: 5px;
}

.tab-nav-btn.right {
  margin-left: 5px;
}

/* 标签容器 - 可滚动区域 */
.tabs-container {
  flex: 1;
  overflow: hidden;
  position: relative;
}

/* 标签包装器 */
.tabs-wrapper {
  display: flex;
  gap: 5px;
  transition: transform 0.3s;
  white-space: nowrap;
}

/* 标签项 */
.tab-item {
  display: inline-flex;
  align-items: center;
  padding: 0 12px;
  height: 32px;
  border: 1px solid #e4e7ed;
  border-radius: 3px;
  background: #fff;
  cursor: pointer;
  transition: all 0.3s;
  flex-shrink: 0;
  white-space: nowrap;
}

/* 标签标题 */
.tab-title {
  display: inline-block;
  max-width: 200px;
  overflow: visible;
  white-space: nowrap;
}

.tab-item:hover {
  background: #f5f7fa;
}

.tab-item.is-active {
  background: #409eff;
  color: #fff;
  border-color: #409eff;
}

/* 关闭按钮 */
.tab-close {
  margin-left: 8px;
  font-size: 12px;
  flex-shrink: 0;
}

.tab-close:hover {
  color: #f56c6c;
}

.tab-item.is-active .tab-close:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
}

/* 主内容区 */
.main-content {
  background: #f5f7fa;
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}
</style>

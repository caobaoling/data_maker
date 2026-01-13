import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useTabsStore = defineStore('tabs', () => {
  // 已访问的标签页
  const visitedTabs = ref([
    {
      path: '/home',
      title: '首页',
      icon: 'HomeFilled',
      affix: true  // 固定标签,不可关闭
    }
  ])

  // 缓存的组件名称
  const cachedViews = ref(['Home'])

  // 添加标签页
  const addTab = (tab) => {
    const exists = visitedTabs.value.find(t => t.path === tab.path)
    if (!exists) {
      visitedTabs.value.push(tab)
      if (tab.cache !== false) {
        cachedViews.value.push(tab.name || tab.title)
      }
    }
    saveToStorage()
  }

  // 关闭标签页
  const closeTab = (tab) => {
    const index = visitedTabs.value.findIndex(t => t.path === tab.path)
    if (index > -1) {
      visitedTabs.value.splice(index, 1)
      const cacheIndex = cachedViews.value.indexOf(tab.name || tab.title)
      if (cacheIndex > -1) {
        cachedViews.value.splice(cacheIndex, 1)
      }
    }
    saveToStorage()
  }

  // 关闭其他标签页
  const closeOtherTabs = (currentTab) => {
    visitedTabs.value = visitedTabs.value.filter(
      tab => tab.affix || tab.path === currentTab.path
    )
    cachedViews.value = [currentTab.name || currentTab.title]
    saveToStorage()
  }

  // 关闭所有标签页
  const closeAllTabs = () => {
    visitedTabs.value = visitedTabs.value.filter(tab => tab.affix)
    cachedViews.value = []
    saveToStorage()
  }

  // 持久化
  const saveToStorage = () => {
    localStorage.setItem('visited-tabs', JSON.stringify(visitedTabs.value))
    localStorage.setItem('cached-views', JSON.stringify(cachedViews.value))
  }

  // 恢复
  const restoreFromStorage = () => {
    const savedTabs = localStorage.getItem('visited-tabs')
    const savedViews = localStorage.getItem('cached-views')
    if (savedTabs) visitedTabs.value = JSON.parse(savedTabs)
    if (savedViews) cachedViews.value = JSON.parse(savedViews)
  }

  return {
    visitedTabs,
    cachedViews,
    addTab,
    closeTab,
    closeOtherTabs,
    closeAllTabs,
    restoreFromStorage
  }
})

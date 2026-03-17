import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '@/layout/MainLayout.vue'

// AI外教路由
const routes = [
  {
    path: '/',
    component: MainLayout,
    redirect: '/home',
    children: [
      {
        path: '/home',
        name: 'Home',
        component: () => import('@/views/Home.vue'),
        meta: { title: '首页', icon: 'HomeFilled', affix: true }
      },
      {
        path: '/appoint/add',
        name: 'AddAppoint',
        component: () => import('@/views/appoint/AddAppoint.vue'),
        meta: { title: '添加预约', icon: 'Plus' }
      },
      {
        path: '/appoint/list',
        name: 'AppointList',
        component: () => import('@/views/appoint/AppointList.vue'),
        meta: { title: '预约列表', icon: 'List' }
      },
      {
        path: '/appoint/star',
        name: 'AddStar',
        component: () => import('@/views/appoint/AddStar.vue'),
        meta: { title: '预约打星', icon: 'Star' }
      },
      {
        path: '/redis/tool',
        name: 'RedisTool',
        component: () => import('@/views/redis/RedisTool.vue'),
        meta: { title: 'Redis工具', icon: 'Coin' }
      },
      {
        path: '/ai/add-point',
        name: 'AddPoint',
        component: () => import('@/views/aiTeacher/AddPoint.vue'),
        meta: { title: '添加财富', icon: 'CoinFilled' }
      },
      {
        path: '/ai/exchange-code',
        name: 'ExchangeCode',
        component: () => import('@/views/aiTeacher/ExchangeCode.vue'),
        meta: { title: '兑换码', icon: 'Ticket' }
      },
      {
        path: '/ai/clear-plan',
        name: 'ClearPlan',
        component: () => import('@/views/aiTeacher/ClearPlan.vue'),
        meta: { title: '清空学习计划', icon: 'Delete' }
      },
      {
        path: '/elf/add-star',
        name: 'ElfAddStar',
        component: () => import('@/views/elf/AddStar.vue'),
        meta: { title: '添加星星', icon: 'Star' }
      },
      {
        path: '/elf/change-level',
        name: 'ElfChangeLevel',
        component: () => import('@/views/elf/ChangeLevel.vue'),
        meta: { title: '修改等级', icon: 'Trophy' }
      },
      {
        path: '/elf/end-class',
        name: 'ElfEndClass',
        component: () => import('@/views/elf/EndClass.vue'),
        meta: { title: '精灵结课', icon: 'Check' }
      },
      // 查询任务功能暂时隐藏 - 接口有问题
      // {
      //   path: '/elf/query-task',
      //   name: 'ElfQueryTask',
      //   component: () => import('@/views/elf/QueryTask.vue'),
      //   meta: { title: '查询任务', icon: 'Search' }
      // },
      {
        path: '/elf/del-task',
        name: 'ElfDelTask',
        component: () => import('@/views/elf/DelTask.vue'),
        meta: { title: '删除任务', icon: 'Delete' }
      },
      {
        path: '/elf/manage-rank',
        name: 'ElfManageRank',
        component: () => import('@/views/elf/ManageRank.vue'),
        meta: { title: '管理排行榜', icon: 'Histogram' }
      },
      {
        path: '/picturebook/clear-plan',
        name: 'PicturebookClearPlan',
        component: () => import('@/views/picturebook/ClearPlan.vue'),
        meta: { title: '清除绘本学习计划', icon: 'Delete' }
      },
      {
        path: '/teacher/contract',
        name: 'TeacherContract',
        component: () => import('@/views/teacher/Contract.vue'),
        meta: { title: '给老师签合同(SA)', icon: 'Document' }
      },
      {
        path: '/user/add-wealth',
        name: 'AddWealth',
        component: () => import('@/views/user/AddWealth.vue'),
        meta: { title: '添加财富', icon: 'Wallet' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

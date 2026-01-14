import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '@/layout/MainLayout.vue'

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
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

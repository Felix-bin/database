import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Layout',
      component: () => import('@/views/Layout.vue'),
      redirect: '/dashboard',
      children: [
        {
          path: '/dashboard',
          name: 'Dashboard',
          component: () => import('@/views/Dashboard.vue'),
          meta: { title: '工作台概览', icon: 'DashboardOutlined' }
        },
        {
          path: '/inventory',
          name: 'Inventory',
          component: () => import('@/views/Inventory.vue'),
          meta: { title: '仓储与库存', icon: 'InboxOutlined' }
        },
        {
          path: '/leasing',
          name: 'Leasing',
          component: () => import('@/views/Leasing.vue'),
          meta: { title: '租赁与出库', icon: 'FileTextOutlined' }
        },
        {
          path: '/return',
          name: 'Return',
          component: () => import('@/views/Return.vue'),
          meta: { title: '归还与质检', icon: 'CheckCircleOutlined' }
        },
        {
          path: '/finance',
          name: 'Finance',
          component: () => import('@/views/Finance.vue'),
          meta: { title: '费用结算', icon: 'DollarOutlined' }
        },
        {
          path: '/settings',
          name: 'Settings',
          component: () => import('@/views/Settings.vue'),
          meta: { title: '系统设置', icon: 'SettingOutlined' }
        }
      ]
    }
  ]
})

export default router


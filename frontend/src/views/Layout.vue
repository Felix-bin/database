<template>
  <div class="app-layout">
    <!-- 侧边栏 -->
    <div class="sidebar" :class="{ collapsed: collapsed }">
      <div class="logo">
        <ShopOutlined style="margin-right: 10px; color: #00a8e8; font-size: 18px" />
        <span v-if="!collapsed">港口装备管理系统</span>
      </div>
      
      <div class="menu">
        <div
          v-for="item in menuItems"
          :key="item.key"
          class="menu-item"
          :class="{ active: selectedKeys.includes(item.key) }"
          @click="handleMenuClick(item)"
        >
          <component :is="item.icon" class="menu-icon" />
          <span v-if="!collapsed">{{ item.title }}</span>
        </div>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="main-content">
      <!-- 顶部栏 -->
      <header>
        <div style="display: flex; align-items: center; gap: 16px">
          <MenuUnfoldOutlined
            v-if="collapsed"
            class="trigger"
            @click="toggleSidebar"
          />
          <MenuFoldOutlined
            v-else
            class="trigger"
            @click="toggleSidebar"
          />
          <h3 style="margin: 0; font-size: 18px; font-weight: 600; color: #2c3e50">{{ pageTitle }}</h3>
        </div>
        
        <div class="user-info">
          <BellOutlined style="font-size: 18px; cursor: pointer; color: #666" />
          <span>操作员：{{ currentUser.realName }}</span>
          <div class="user-avatar">
            <UserOutlined />
          </div>
        </div>
      </header>

      <!-- 内容区 -->
      <div class="content-area">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAppStore } from '@/stores/app'
import {
  DashboardOutlined,
  InboxOutlined,
  FileTextOutlined,
  CheckCircleOutlined,
  DollarOutlined,
  SettingOutlined,
  MenuUnfoldOutlined,
  MenuFoldOutlined,
  BellOutlined,
  UserOutlined,
  ShopOutlined
} from '@ant-design/icons-vue'

const router = useRouter()
const route = useRoute()
const appStore = useAppStore()

const collapsed = computed({
  get: () => appStore.collapsed,
  set: (val) => appStore.collapsed = val
})

const currentUser = computed(() => appStore.currentUser)
const selectedKeys = ref([route.path])

const menuItems = [
  { key: '/dashboard', title: '工作台', icon: DashboardOutlined },
  { key: '/inventory', title: '仓储与库存', icon: InboxOutlined },
  { key: '/leasing', title: '租赁与出库', icon: FileTextOutlined },
  { key: '/return', title: '归还与检验', icon: CheckCircleOutlined },
  { key: '/finance', title: '费用结算', icon: DollarOutlined },
  { key: '/settings', title: '系统设置', icon: SettingOutlined }
]

const pageTitle = computed(() => {
  const titles = {
    '/dashboard': '工作台概览',
    '/inventory': '仓储与库存管理',
    '/leasing': '租赁作业与出库',
    '/return': '设备归还与质检',
    '/finance': '财务费用结算',
    '/settings': '系统设置'
  }
  return titles[route.path] || '系统'
})

watch(() => route.path, (newPath) => {
  selectedKeys.value = [newPath]
})

const toggleSidebar = () => {
  appStore.toggleSidebar()
}

const handleMenuClick = (item) => {
  router.push(item.key)
}
</script>

<style scoped>
.app-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

/* 侧边栏样式 */
.sidebar {
  width: var(--sidebar-width);
  background-color: #1a2530;
  color: white;
  display: flex;
  flex-direction: column;
  transition: all 0.3s;
}

.sidebar.collapsed {
  width: 80px;
}

.logo {
  height: var(--header-height);
  display: flex;
  align-items: center;
  padding: 0 20px;
  font-size: 18px;
  font-weight: bold;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  background-color: #131b24;
}

.menu {
  flex: 1;
  padding-top: 20px;
}

.menu-item {
  padding: 15px 25px;
  cursor: pointer;
  transition: 0.2s;
  display: flex;
  align-items: center;
  color: #aeb9c6;
  text-decoration: none;
}

.menu-item:hover,
.menu-item.active {
  background-color: var(--primary-color);
  color: white;
  border-left: 4px solid var(--accent-color);
}

.menu-icon {
  margin-right: 12px;
  width: 20px;
  text-align: center;
  font-size: 16px;
}

.sidebar.collapsed .menu-icon {
  margin-right: 0;
}

/* 主内容区 */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 顶部栏 */
header {
  height: var(--header-height);
  background: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 30px;
  box-shadow: var(--card-shadow);
  z-index: 10;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.user-avatar {
  width: 35px;
  height: 35px;
  background: #ddd;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
}

.trigger {
  font-size: 18px;
  cursor: pointer;
  transition: color 0.3s;
  color: #666;
}

.trigger:hover {
  color: var(--primary-color);
}

/* 内容区 */
.content-area {
  flex: 1;
  padding: 25px;
  overflow-y: auto;
  background-color: var(--bg-color);
}

/* 动画 */
.fade-enter-active,
.fade-leave-active {
  animation: fadeIn 0.4s;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>


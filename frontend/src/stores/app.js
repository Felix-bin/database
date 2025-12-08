import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  const collapsed = ref(false)
  const currentUser = ref({
    username: 'zhanggong',
    realName: '张工',
    role: 'operator'
  })

  const toggleSidebar = () => {
    collapsed.value = !collapsed.value
  }

  return {
    collapsed,
    currentUser,
    toggleSidebar
  }
})


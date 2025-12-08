import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Antd from 'ant-design-vue'
import * as Icons from '@ant-design/icons-vue'
import router from './router'
import App from './App.vue'

import 'ant-design-vue/dist/reset.css'
import './style.css'

const app = createApp(App)
const pinia = createPinia()

// 注册所有图标
Object.keys(Icons).forEach(key => {
  app.component(key, Icons[key])
})

app.use(pinia)
app.use(router)
app.use(Antd)

app.mount('#app')


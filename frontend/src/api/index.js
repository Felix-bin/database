import axios from 'axios'
import { message } from 'ant-design-vue'

// 创建 axios 实例
const request = axios.create({
  baseURL: '/api',
  timeout: 30000
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    // 可以在这里添加token
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    message.error(error.response?.data?.detail || '请求失败')
    return Promise.reject(error)
  }
)

// API 接口定义

// 工作台统计
export const getDashboardStats = () => request.get('/dashboard/stats')

// 设备管理
export const getEquipmentList = (params) => request.get('/equipment', { params })
export const getEquipmentDetail = (id) => request.get(`/equipment/${id}`)
export const createEquipment = (data) => request.post('/equipment', data)
export const updateEquipment = (id, data) => request.put(`/equipment/${id}`, data)
export const deleteEquipment = (id) => request.delete(`/equipment/${id}`)

// 客户管理
export const getCustomerList = (params) => request.get('/customers', { params })
export const createCustomer = (data) => request.post('/customers', data)

// 订单管理
export const getOrderList = (params) => request.get('/orders', { params })
export const getOrderDetail = (id) => request.get(`/orders/${id}`)
export const createOrder = (data) => request.post('/orders', data)
export const updateOrder = (id, data) => request.put(`/orders/${id}`, data)

// 账单管理
export const getBillingList = (params) => request.get('/billing', { params })
export const createBilling = (data) => request.post('/billing', data)
export const updateBilling = (id, data) => request.put(`/billing/${id}`, data)

// 归还与质检
export const createReturn = (data) => request.post('/returns', data)
export const createInspection = (data) => request.post('/inspections', data)

// 认证相关
export const login = (data) => request.post('/auth/login', data)
export const register = (data) => request.post('/auth/register', data)

export default request


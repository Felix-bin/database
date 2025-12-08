<template>
  <div>
    <!-- 新建租赁申请 -->
    <div class="table-container" style="margin-bottom: 20px">
      <h4 style="margin-bottom: 15px; color: var(--primary-color)">
        <PlusCircleOutlined style="margin-right: 8px" /> 新建租赁申请
      </h4>
      <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 15px">
        <div>
          <label style="font-size: 12px; color: #666; display: block; margin-bottom: 5px">申请船舶/客户</label>
          <a-select
            v-model:value="newOrder.customer_name"
            style="width: 100%"
            placeholder="选择客户"
          >
            <a-select-option value="长宏海运 - 远大号">长宏海运 - 远大号</a-select-option>
            <a-select-option value="远洋荣耀号">远洋荣耀号</a-select-option>
            <a-select-option value="太平洋航运">太平洋航运</a-select-option>
            <a-select-option value="马士基物流">马士基物流</a-select-option>
          </a-select>
        </div>
        <div>
          <label style="font-size: 12px; color: #666; display: block; margin-bottom: 5px">航次号 (Voyage No.)</label>
          <a-input v-model:value="newOrder.voyage_no" placeholder="CH-20231024" />
        </div>
        <div>
          <label style="font-size: 12px; color: #666; display: block; margin-bottom: 5px">预计使用时间</label>
          <a-date-picker v-model:value="newOrder.start_date" style="width: 100%" />
        </div>
        <div style="display: flex; align-items: flex-end">
          <a-button type="primary" style="width: 100%" @click="showSelectEquipment">
            <template #icon><PlusOutlined /></template>
            创建订单并选配设备
          </a-button>
        </div>
      </div>
      <p style="margin-top: 10px; font-size: 12px; color: #999">
        <InfoCircleOutlined /> 系统将自动执行触发器：trg_create_lease_order
      </p>
    </div>

    <!-- 订单列表 -->
    <div class="table-container">
      <div class="table-header">
        <h4>租赁订单列表</h4>
        <div>
          <a-button style="margin-right: 10px" @click="showFilterModal">
            <template #icon><FilterOutlined /></template>
            筛选
          </a-button>
          <a-button>
            <template #icon><ExportOutlined /></template>
            导出
          </a-button>
        </div>
      </div>

      <div style="margin-bottom: 16px; display: flex; gap: 10px">
        <a-input-search
          v-model:value="searchKeyword"
          placeholder="搜索订单号/客户/航次"
          style="width: 300px"
          @search="handleSearch"
        />
        <a-select
          v-model:value="filterStatus"
          style="width: 150px"
          placeholder="订单状态"
          allowClear
          @change="handleSearch"
        >
          <a-select-option value="">全部</a-select-option>
          <a-select-option value="待提货">待提货</a-select-option>
          <a-select-option value="航次执行中">航次执行中</a-select-option>
          <a-select-option value="已完结">已完结</a-select-option>
        </a-select>
      </div>

      <table class="data-table">
        <thead>
          <tr>
            <th>订单号</th>
            <th>申请单位</th>
            <th>航次号</th>
            <th>包含设备数</th>
            <th>起租时间</th>
            <th>预计归还</th>
            <th>流程状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in tableData" :key="item.order_id">
            <td>{{ item.order_code }}</td>
            <td>{{ item.customer_name }}</td>
            <td>{{ item.voyage_no || '-' }}</td>
            <td>
              <a @click="showEquipmentList(item)" style="color: var(--primary-color); font-weight: bold">
                {{ item.equipment_count || 0 }} 件
              </a>
            </td>
            <td>{{ formatDate(item.start_date) }}</td>
            <td>{{ formatDate(item.expected_return_date) }}</td>
            <td><span :class="getStatusBadgeClass(item.status)">{{ item.status }}</span></td>
            <td>
              <a-button
                v-if="item.status === '待提货'"
                type="primary"
                size="small"
                style="margin-right: 8px"
                @click="handleCheckout(item)"
              >
                办理出库
              </a-button>
              <a @click="viewDetail(item)" style="margin-right: 8px">详情</a>
              <a v-if="item.status === '航次执行中'" @click="showTracking(item)">追踪</a>
            </td>
          </tr>
        </tbody>
      </table>

      <div style="margin-top: 15px; display: flex; justify-content: space-between; align-items: center">
        <span style="color: #666; font-size: 14px">
          显示 {{ (pagination.current - 1) * pagination.pageSize + 1 }}-{{ Math.min(pagination.current * pagination.pageSize, pagination.total) }} / 共 {{ pagination.total }} 条
        </span>
        <a-pagination
          v-model:current="pagination.current"
          v-model:page-size="pagination.pageSize"
          :total="pagination.total"
          size="small"
          @change="handleTableChange"
        />
      </div>
    </div>

    <!-- 选配设备模态框 -->
    <a-modal
      v-model:open="equipmentModalVisible"
      title="选配设备"
      width="800px"
      @ok="handleCreateOrder"
    >
      <a-table
        :columns="equipmentColumns"
        :data-source="availableEquipment"
        :row-selection="rowSelection"
        :pagination="false"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'rental_days'">
            <a-input-number v-model:value="record.rental_days" :min="1" :max="365" />
          </template>
        </template>
      </a-table>
      <div style="margin-top: 16px; padding: 12px; background: #e7f3ff; border-radius: 4px">
        <strong>已选择：{{ selectedEquipmentIds.length }} 件设备</strong>
      </div>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { message } from 'ant-design-vue'
import {
  PlusOutlined,
  PlusCircleOutlined,
  InfoCircleOutlined,
  FilterOutlined,
  ExportOutlined
} from '@ant-design/icons-vue'
import { getOrderList, createOrder, getEquipmentList } from '@/api'
import dayjs from 'dayjs'

const columns = [
  { title: '订单号', dataIndex: 'order_code', key: 'order_code' },
  { title: '申请单位', dataIndex: 'customer_name', key: 'customer_name' },
  { title: '航次号', dataIndex: 'voyage_no', key: 'voyage_no' },
  { title: '起租时间', dataIndex: 'start_date', key: 'start_date' },
  { title: '预计归还', dataIndex: 'expected_return_date', key: 'expected_return_date' },
  { title: '流程状态', dataIndex: 'status', key: 'status' },
  { title: '操作', key: 'action', width: 200 }
]

const equipmentColumns = [
  { title: '设备编号', dataIndex: 'equipment_code', key: 'equipment_code' },
  { title: '设备名称', dataIndex: 'equipment_name', key: 'equipment_name' },
  { title: '类别', dataIndex: 'category', key: 'category' },
  { title: '日租金', dataIndex: 'daily_rental_rate', key: 'daily_rental_rate' },
  { title: '租用天数', key: 'rental_days', width: 120 }
]

const tableData = ref([])
const loading = ref(false)
const searchKeyword = ref('')
const filterStatus = ref('')

const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
  showTotal: (total) => `共 ${total} 条`
})

const newOrder = ref({
  customer_name: '',
  voyage_no: '',
  start_date: null
})

const equipmentModalVisible = ref(false)
const availableEquipment = ref([])
const selectedEquipmentIds = ref([])
const selectedEquipment = ref([])

const rowSelection = computed(() => ({
  selectedRowKeys: selectedEquipmentIds.value,
  onChange: (selectedRowKeys, selectedRows) => {
    selectedEquipmentIds.value = selectedRowKeys
    selectedEquipment.value = selectedRows
  }
}))

const getStatusBadgeClass = (status) => {
  const classMap = {
    '待提货': 'badge badge-info',
    '航次执行中': 'badge badge-warning',
    '已完结': 'badge badge-success'
  }
  return classMap[status] || 'badge'
}

const formatDate = (date) => {
  if (!date) return '-'
  return dayjs(date).format('YYYY-MM-DD')
}

const showFilterModal = () => {
  message.info('筛选功能待完善')
}

const showEquipmentList = (record) => {
  message.info('设备清单功能待完善')
}

const showTracking = (record) => {
  message.info('设备追踪功能待完善')
}

const loadData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.current,
      page_size: pagination.pageSize,
      keyword: searchKeyword.value || undefined,
      status: filterStatus.value || undefined
    }
    const res = await getOrderList(params)
    tableData.value = res.data
    pagination.total = res.total
  } catch (error) {
    message.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

const loadAvailableEquipment = async () => {
  try {
    const res = await getEquipmentList({
      status: '在库',
      page: 1,
      page_size: 100
    })
    availableEquipment.value = res.data.map(item => ({
      ...item,
      key: item.equipment_id,
      rental_days: 30
    }))
  } catch (error) {
    message.error('加载可用设备失败')
  }
}

const handleTableChange = (page, pageSize) => {
  pagination.current = page
  pagination.pageSize = pageSize
  loadData()
}

const handleSearch = () => {
  pagination.current = 1
  loadData()
}

const showSelectEquipment = () => {
  if (!newOrder.value.customer_name || !newOrder.value.start_date) {
    message.warning('请先填写客户名称和起租日期')
    return
  }
  equipmentModalVisible.value = true
  loadAvailableEquipment()
}

const handleCreateOrder = async () => {
  if (selectedEquipment.value.length === 0) {
    message.warning('请至少选择一件设备')
    return
  }

  try {
    const orderData = {
      customer_id: 1, // 这里应该根据客户名称查找ID
      customer_name: newOrder.value.customer_name,
      voyage_no: newOrder.value.voyage_no,
      start_date: dayjs(newOrder.value.start_date).format('YYYY-MM-DD'),
      expected_return_date: dayjs(newOrder.value.start_date).add(30, 'day').format('YYYY-MM-DD'),
      order_items: selectedEquipment.value.map(item => ({
        equipment_id: item.equipment_id,
        equipment_code: item.equipment_code,
        equipment_name: item.equipment_name,
        daily_rate: item.daily_rental_rate,
        rental_days: item.rental_days || 30
      }))
    }

    await createOrder(orderData)
    message.success('订单创建成功')
    equipmentModalVisible.value = false
    selectedEquipmentIds.value = []
    loadData()
  } catch (error) {
    message.error('创建订单失败')
  }
}

const viewDetail = (record) => {
  message.info('订单详情功能待完善')
}

const handleCheckout = (record) => {
  message.info('出库办理功能待完善')
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.data-table th {
  background-color: #f8f9fa;
  color: #555;
  font-weight: 600;
}

.data-table tr:hover {
  background-color: #f1f7fd;
}

.data-table a {
  color: var(--primary-color);
  text-decoration: none;
}

.data-table a:hover {
  text-decoration: underline;
}
</style>


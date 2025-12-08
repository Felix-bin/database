<template>
  <div>
    <!-- 统计卡片 -->
    <div class="dashboard-grid" style="grid-template-columns: repeat(3, 1fr); margin-bottom: 20px">
      <div class="stat-card">
        <div class="stat-info">
          <h3>¥ 458,600</h3>
          <p>本月总收入</p>
        </div>
        <div class="stat-icon"><LineChartOutlined /></div>
      </div>
      <div class="stat-card">
        <div class="stat-info">
          <h3>¥ 126,300</h3>
          <p>待结算金额</p>
        </div>
        <div class="stat-icon"><ClockCircleOutlined /></div>
      </div>
      <div class="stat-card">
        <div class="stat-info">
          <h3>15</h3>
          <p>逾期未付</p>
        </div>
        <div class="stat-icon" style="color: var(--danger); opacity: 1"><ExclamationTriangleOutlined /></div>
      </div>
    </div>

    <!-- 账单列表 -->
    <div class="table-container">
      <div class="table-header">
        <h4>费用结算中心</h4>
        <div>
          <a-button style="margin-right: 10px" @click="showFilterModal">
            <template #icon><FilterOutlined /></template>
            筛选
          </a-button>
          <a-button style="margin-right: 10px">
            <template #icon><ExportOutlined /></template>
            导出月度报表
          </a-button>
          <a-button type="primary" @click="showAddModal">
            <template #icon><PlusOutlined /></template>
            新建账单
          </a-button>
        </div>
      </div>

      <div style="margin-bottom: 16px; display: flex; gap: 10px">
        <a-input-search
          v-model:value="searchKeyword"
          placeholder="搜索账单号/客户"
          style="width: 300px"
          @search="handleSearch"
        />
        <a-select
          v-model:value="filterStatus"
          placeholder="账单状态"
          style="width: 150px"
          allowClear
          @change="handleSearch"
        >
          <a-select-option value="">全部</a-select-option>
          <a-select-option value="待确认">待确认</a-select-option>
          <a-select-option value="已确认">已确认</a-select-option>
          <a-select-option value="已结清">已结清</a-select-option>
          <a-select-option value="逾期">逾期</a-select-option>
        </a-select>
      </div>

      <table class="data-table">
        <thead>
          <tr>
            <th>账单编号</th>
            <th>客户名称</th>
            <th>关联订单/航次</th>
            <th>租赁费用</th>
            <th>维修/赔偿费</th>
            <th>总金额</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in tableData" :key="item.bill_id">
            <td>{{ item.bill_code }}</td>
            <td>{{ item.customer_name }}</td>
            <td>{{ item.order_code || '-' }}</td>
            <td>¥ {{ (item.rental_fee || 0).toFixed(2) }}</td>
            <td>¥ {{ (item.repair_fee || 0).toFixed(2) }}</td>
            <td><strong style="color: var(--primary-color)">¥ {{ (item.total_amount || 0).toFixed(2) }}</strong></td>
            <td><span :class="getStatusBadgeClass(item.status)">{{ item.status }}</span></td>
            <td>
              <a @click="viewDetail(item)" style="margin-right: 8px">详情</a>
              <a-button
                v-if="item.status === '待确认'"
                type="text"
                size="small"
                @click="confirmBilling(item)"
              >
                发送账单
              </a-button>
              <a-button
                v-else-if="item.status === '已结清'"
                type="text"
                size="small"
              >
                查看发票
              </a-button>
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

    <!-- 新增/编辑账单模态框 -->
    <a-modal
      v-model:open="modalVisible"
      :title="modalTitle"
      @ok="handleSubmit"
      width="600px"
    >
      <a-form
        :model="formData"
        :label-col="{ span: 6 }"
        :wrapper-col="{ span: 16 }"
      >
        <a-form-item label="客户名称" required>
          <a-input v-model:value="formData.customer_name" />
        </a-form-item>
        <a-form-item label="租赁费用">
          <a-input-number
            v-model:value="formData.rental_fee"
            :min="0"
            :precision="2"
            style="width: 100%"
            prefix="¥"
          />
        </a-form-item>
        <a-form-item label="维修/赔偿费">
          <a-input-number
            v-model:value="formData.repair_fee"
            :min="0"
            :precision="2"
            style="width: 100%"
            prefix="¥"
          />
        </a-form-item>
        <a-form-item label="其他费用">
          <a-input-number
            v-model:value="formData.other_fee"
            :min="0"
            :precision="2"
            style="width: 100%"
            prefix="¥"
          />
        </a-form-item>
        <a-form-item label="总金额">
          <a-input-number
            :value="totalAmount"
            disabled
            :precision="2"
            style="width: 100%"
            prefix="¥"
          />
        </a-form-item>
        <a-form-item label="备注">
          <a-textarea v-model:value="formData.remarks" :rows="3" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import {
  PlusOutlined,
  ExportOutlined,
  FilterOutlined,
  LineChartOutlined,
  ClockCircleOutlined,
  ExclamationTriangleOutlined
} from '@ant-design/icons-vue'
import { getBillingList, createBilling, updateBilling } from '@/api'

const columns = [
  { title: '账单编号', dataIndex: 'bill_code', key: 'bill_code' },
  { title: '客户名称', dataIndex: 'customer_name', key: 'customer_name' },
  { title: '租赁费用', dataIndex: 'rental_fee', key: 'rental_fee' },
  { title: '维修/赔偿费', dataIndex: 'repair_fee', key: 'repair_fee' },
  { title: '总金额', dataIndex: 'total_amount', key: 'total_amount' },
  { title: '状态', dataIndex: 'status', key: 'status' },
  { title: '操作', key: 'action', width: 200 }
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

const modalVisible = ref(false)
const modalTitle = ref('新建账单')
const isEdit = ref(false)
const formData = ref({
  customer_name: '',
  rental_fee: 0,
  repair_fee: 0,
  other_fee: 0,
  remarks: '',
  order_id: 1 // 这里应该关联实际订单
})

const totalAmount = computed(() => {
  return (formData.value.rental_fee || 0) +
         (formData.value.repair_fee || 0) +
         (formData.value.other_fee || 0)
})

const getStatusBadgeClass = (status) => {
  const classMap = {
    '待确认': 'badge badge-info',
    '已确认': 'badge badge-info',
    '已结清': 'badge badge-success',
    '逾期': 'badge badge-danger'
  }
  return classMap[status] || 'badge'
}

const showFilterModal = () => {
  message.info('筛选功能待完善')
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
    const res = await getBillingList(params)
    tableData.value = res.data
    pagination.total = res.total
  } catch (error) {
    message.error('加载数据失败')
  } finally {
    loading.value = false
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

const showAddModal = () => {
  modalVisible.value = true
  modalTitle.value = '新建账单'
  isEdit.value = false
  formData.value = {
    customer_name: '',
    rental_fee: 0,
    repair_fee: 0,
    other_fee: 0,
    remarks: '',
    order_id: 1
  }
}

const showEditModal = (record) => {
  modalVisible.value = true
  modalTitle.value = '编辑账单'
  isEdit.value = true
  formData.value = { ...record }
}

const handleSubmit = async () => {
  try {
    if (isEdit.value) {
      await updateBilling(formData.value.bill_id, formData.value)
      message.success('更新成功')
    } else {
      await createBilling(formData.value)
      message.success('创建成功')
    }
    modalVisible.value = false
    loadData()
  } catch (error) {
    message.error('操作失败')
  }
}

const viewDetail = (record) => {
  message.info('账单详情功能待完善')
}

const confirmBilling = async (record) => {
  try {
    await updateBilling(record.bill_id, { status: '已确认' })
    message.success('账单已确认')
    loadData()
  } catch (error) {
    message.error('操作失败')
  }
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


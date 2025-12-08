<template>
  <div>
    <!-- 流程步骤 -->
    <div class="process-steps">
      <div class="step active">
        <PlusOutlined />
        <p>采购入库</p>
      </div>
      <div class="step active">
        <BarcodeOutlined />
        <p>编码贴标</p>
      </div>
      <div class="step active">
        <HomeOutlined />
        <p>库位分配</p>
      </div>
      <div class="step">
        <ToolOutlined />
        <p>定期维保</p>
      </div>
    </div>

    <!-- 设备列表 -->
    <div class="table-container">
      <div class="table-header">
        <div>
          <a-button type="primary" @click="showAddModal" style="margin-right: 10px">
            <template #icon><PlusOutlined /></template>
            新设备入库
          </a-button>
          <a-button style="margin-right: 10px">
            <template #icon><UploadOutlined /></template>
            批量导入
          </a-button>
          <a-button @click="refreshView">
            <template #icon><ReloadOutlined /></template>
            刷新库存视图
          </a-button>
        </div>
        <div>
          <a-input-search
            v-model:value="searchKeyword"
            placeholder="搜索设备名称/编号..."
            style="width: 250px; margin-right: 10px"
            @search="handleSearch"
          />
          <a-button @click="showFilterModal">
            <template #icon><FilterOutlined /></template>
            高级筛选
          </a-button>
        </div>
      </div>

      <table class="data-table">
        <thead>
          <tr>
            <th><input type="checkbox" /></th>
            <th>设备编号</th>
            <th>名称/型号</th>
            <th>类别</th>
            <th>存放库位</th>
            <th>入库日期</th>
            <th>当前状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in tableData" :key="item.equipment_id">
            <td><input type="checkbox" /></td>
            <td>{{ item.equipment_code }}</td>
            <td>{{ item.equipment_name }}</td>
            <td>{{ item.category }}</td>
            <td>{{ item.storage_location || '-' }}</td>
            <td>{{ formatDate(item.created_at) }}</td>
            <td><span :class="getStatusBadgeClass(item.status)">{{ item.status }}</span></td>
            <td>
              <a @click="showDetailModal(item)" style="margin-right: 8px">详情</a>
              <a @click="showEditModal(item)" style="margin-right: 8px">编辑</a>
              <a @click="handleMove(item)" style="margin-right: 8px">移库</a>
            </td>
          </tr>
        </tbody>
      </table>

      <div style="margin-top: 15px; display: flex; justify-content: space-between; align-items: center">
        <div>
          <a-button type="text" @click="handleBatchDelete" style="margin-right: 10px">批量删除</a-button>
          <a-button type="text">批量导出</a-button>
        </div>
        <div>
          <span style="color: #666; font-size: 14px; margin-right: 15px">
            显示 {{ (pagination.current - 1) * pagination.pageSize + 1 }}-{{ Math.min(pagination.current * pagination.pageSize, pagination.total) }} / 共 {{ pagination.total }} 条
          </span>
          <a-pagination
            v-model:current="pagination.current"
            v-model:page-size="pagination.pageSize"
            :total="pagination.total"
            :show-size-changer="true"
            :page-size-options="['10', '20', '50', '100']"
            size="small"
            @change="handleTableChange"
          />
        </div>
      </div>
    </div>

    <!-- 新增/编辑设备模态框 -->
    <a-modal
      v-model:open="modalVisible"
      :title="modalTitle"
      @ok="handleSubmit"
      @cancel="handleCancel"
      width="600px"
    >
      <a-form
        :model="formData"
        :label-col="{ span: 6 }"
        :wrapper-col="{ span: 16 }"
      >
        <a-form-item label="设备编号" required>
          <a-input v-model:value="formData.equipment_code" :disabled="isEdit" />
        </a-form-item>
        <a-form-item label="设备名称" required>
          <a-input v-model:value="formData.equipment_name" />
        </a-form-item>
        <a-form-item label="设备类别" required>
          <a-select v-model:value="formData.category">
            <a-select-option value="起重配件">起重配件</a-select-option>
            <a-select-option value="流体设备">流体设备</a-select-option>
            <a-select-option value="固缚索具">固缚索具</a-select-option>
            <a-select-option value="液压工具">液压工具</a-select-option>
            <a-select-option value="装卸工具">装卸工具</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="库位">
          <a-input v-model:value="formData.storage_location" placeholder="如：A区-01-04" />
        </a-form-item>
        <a-form-item label="采购价格">
          <a-input-number
            v-model:value="formData.purchase_price"
            :min="0"
            :precision="2"
            style="width: 100%"
            prefix="¥"
          />
        </a-form-item>
        <a-form-item label="日租金">
          <a-input-number
            v-model:value="formData.daily_rental_rate"
            :min="0"
            :precision="2"
            style="width: 100%"
            prefix="¥"
          />
        </a-form-item>
        <a-form-item label="规格说明">
          <a-textarea v-model:value="formData.specifications" :rows="3" />
        </a-form-item>
        <a-form-item label="备注">
          <a-textarea v-model:value="formData.remarks" :rows="2" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import {
  PlusOutlined,
  UploadOutlined,
  ReloadOutlined,
  FilterOutlined,
  BarcodeOutlined,
  HomeOutlined,
  ToolOutlined
} from '@ant-design/icons-vue'
import { getEquipmentList, createEquipment, updateEquipment, deleteEquipment } from '@/api'
import dayjs from 'dayjs'

const tableData = ref([
  {
    equipment_id: 1,
    equipment_code: 'CR-5001',
    equipment_name: '门座式起重机配件包',
    category: '起重配件',
    storage_location: 'A区-01-04',
    created_at: '2023-08-10',
    status: '在库'
  },
  {
    equipment_id: 2,
    equipment_code: 'FL-2002',
    equipment_name: '重油输送泵',
    category: '流体设备',
    storage_location: 'B区-02-11',
    created_at: '2023-09-01',
    status: '维修中'
  },
  {
    equipment_id: 3,
    equipment_code: 'CN-1022',
    equipment_name: '绑扎杆 (100根/组)',
    category: '固缚索具',
    storage_location: '-',
    created_at: '2023-01-15',
    status: '已出库'
  },
  {
    equipment_id: 4,
    equipment_code: 'HY-3305',
    equipment_name: '液压千斤顶 (50T)',
    category: '液压工具',
    storage_location: 'C区-03-08',
    created_at: '2023-10-01',
    status: '在库'
  }
])

const loading = ref(false)
const searchKeyword = ref('')
const filterCategory = ref('')
const filterStatus = ref('')

const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 124
})

const modalVisible = ref(false)
const modalTitle = ref('新设备入库')
const isEdit = ref(false)
const formData = ref({
  equipment_code: '',
  equipment_name: '',
  category: '',
  storage_location: '',
  purchase_price: 0,
  daily_rental_rate: 0,
  specifications: '',
  remarks: ''
})

const getStatusBadgeClass = (status) => {
  const classMap = {
    '在库': 'badge badge-success',
    '已出库': 'badge badge-warning',
    '维修中': 'badge badge-danger',
    '已报废': 'badge'
  }
  return classMap[status] || 'badge'
}

const formatDate = (date) => {
  if (!date) return '-'
  return dayjs(date).format('YYYY-MM-DD')
}

const refreshView = () => {
  message.success('库存统计视图已刷新')
  loadData()
}

const showFilterModal = () => {
  message.info('高级筛选功能待完善')
}

const handleMove = (record) => {
  message.info('移库功能待完善')
}

const handleBatchDelete = () => {
  message.success('批量删除功能待完善')
}

const loadData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.current,
      page_size: pagination.pageSize,
      keyword: searchKeyword.value || undefined,
      category: filterCategory.value || undefined,
      status: filterStatus.value || undefined
    }
    const res = await getEquipmentList(params)
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
  modalTitle.value = '新设备入库'
  isEdit.value = false
  formData.value = {
    equipment_code: '',
    equipment_name: '',
    category: '',
    storage_location: '',
    purchase_price: 0,
    daily_rental_rate: 0,
    specifications: '',
    remarks: ''
  }
}

const showEditModal = (record) => {
  modalVisible.value = true
  modalTitle.value = '编辑设备信息'
  isEdit.value = true
  formData.value = { ...record }
}

const showDetailModal = (record) => {
  message.info('设备详情功能待完善')
}

const handleSubmit = async () => {
  try {
    if (isEdit.value) {
      await updateEquipment(formData.value.equipment_id, formData.value)
      message.success('更新成功')
    } else {
      await createEquipment(formData.value)
      message.success('添加成功')
    }
    modalVisible.value = false
    loadData()
  } catch (error) {
    message.error('操作失败')
  }
}

const handleCancel = () => {
  modalVisible.value = false
}

const handleDelete = async (id) => {
  try {
    await deleteEquipment(id)
    message.success('删除成功')
    loadData()
  } catch (error) {
    message.error('删除失败')
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.process-steps {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30px;
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: var(--card-shadow);
}

.step {
  text-align: center;
  position: relative;
  flex: 1;
}

.step :deep(.anticon) {
  width: 40px;
  height: 40px;
  background: #e9ecef;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 10px;
  color: #6c757d;
  font-size: 18px;
}

.step.active :deep(.anticon) {
  background: var(--primary-color);
  color: white;
}

.step::after {
  content: '';
  position: absolute;
  top: 20px;
  right: -50%;
  width: 100%;
  height: 2px;
  background: #e9ecef;
  z-index: 0;
}

.step:last-child::after {
  display: none;
}

.step p {
  font-size: 13px;
  font-weight: 600;
  color: #555;
  margin: 0;
}

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


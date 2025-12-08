<template>
  <div>
    <div class="dashboard-grid" style="grid-template-columns: 2fr 1fr; margin-bottom: 20px">
      <!-- 归还待检列表 -->
      <div class="table-container">
        <div class="table-header">
          <h4><CheckCircleOutlined style="color: var(--primary-color); margin-right: 8px" /> 归还待检列表</h4>
          <a-button @click="showFilterModal">
            <template #icon><FilterOutlined /></template>
            筛选
          </a-button>
        </div>
        <table class="data-table">
          <thead>
            <tr>
              <th>归还单号</th>
              <th>来源订单</th>
              <th>航次号</th>
              <th>设备数量</th>
              <th>归还时间</th>
              <th>状态</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in mockData" :key="item.key">
              <td>{{ item.return_code }}</td>
              <td>{{ item.order_code }}</td>
              <td>{{ item.voyage_no }}</td>
              <td>
                <a @click="showEquipmentList(item)" style="color: var(--primary-color); font-weight: bold">
                  {{ item.equipment_count }} 件
                </a>
              </td>
              <td>{{ item.return_date }}</td>
              <td><span :class="getStatusBadgeClass(item.status)">{{ item.status }}</span></td>
              <td>
                <a-button
                  v-if="item.status === '待质检'"
                  type="primary"
                  size="small"
                  @click="startInspection(item)"
                >
                  开始质检
                </a-button>
                <a-button
                  v-else
                  size="small"
                  @click="continueInspection(item)"
                >
                  继续质检
                </a-button>
              </td>
            </tr>
          </tbody>
        </table>
        <p style="margin-top: 10px; font-size: 12px; color: #999">
          <DatabaseOutlined /> 数据查询：v_return_inspection_queue (视图)
        </p>
      </div>

      <!-- 快速质检录入 -->
      <div class="table-container" style="border-left: 4px solid var(--accent-color)">
        <h4><FileTextOutlined style="color: var(--primary-color); margin-right: 8px" /> 快速质检录入</h4>
        <div style="margin-top: 15px">
          <p style="font-size: 13px; margin-bottom: 10px; color: #666">
            <InfoCircleOutlined /> 选择归还单开始质检
          </p>
          <p style="font-size: 14px; margin-bottom: 5px"><strong>当前设备：</strong>重型吊索组</p>
          <p style="font-size: 14px; margin-bottom: 15px"><strong>编号：</strong>EQ-2023001</p>

          <label style="display: block; margin-bottom: 5px; font-size: 13px">外观状况</label>
          <a-select v-model:value="inspectionData.appearance_status" style="width: 100%; margin-bottom: 10px">
            <a-select-option value="完好">完好</a-select-option>
            <a-select-option value="轻微磨损">轻微磨损</a-select-option>
            <a-select-option value="严重损坏">严重损坏</a-select-option>
          </a-select>

          <label style="display: block; margin-bottom: 5px; font-size: 13px">功能测试</label>
          <a-radio-group v-model:value="inspectionData.function_test" style="margin-bottom: 15px">
            <a-radio value="通过">通过</a-radio>
            <a-radio value="故障">故障</a-radio>
          </a-radio-group>

          <label style="display: block; margin-bottom: 5px; font-size: 13px">需维修</label>
          <a-switch v-model:checked="needRepair" style="margin-bottom: 15px" />

          <label style="display: block; margin-bottom: 5px; font-size: 13px">处理意见</label>
          <a-textarea v-model:value="inspectionData.remarks" :rows="3" style="margin-bottom: 10px" />

          <a-button type="primary" block @click="handleSubmitInspection">
            确认入库并生成账单
          </a-button>
          <p style="margin-top: 10px; font-size: 11px; color: #999; text-align: center">
            将触发：trg_return_complete + sp_generate_bill
          </p>
        </div>
      </div>
    </div>

    <!-- 质检统计 -->
    <div class="dashboard-grid" style="grid-template-columns: repeat(4, 1fr); margin-bottom: 20px">
      <div class="stat-card">
        <div class="stat-info">
          <h3>15</h3>
          <p>待质检设备</p>
        </div>
        <div class="stat-icon"><ClockCircleOutlined /></div>
      </div>
      <div class="stat-card">
        <div class="stat-info">
          <h3>8</h3>
          <p>质检中</p>
        </div>
        <div class="stat-icon"><LoadingOutlined /></div>
      </div>
      <div class="stat-card">
        <div class="stat-info">
          <h3>142</h3>
          <p>本月已归还</p>
        </div>
        <div class="stat-icon"><CheckCircleOutlined /></div>
      </div>
      <div class="stat-card">
        <div class="stat-info">
          <h3>5</h3>
          <p>需维修设备</p>
        </div>
        <div class="stat-icon" style="color: var(--danger); opacity: 1"><ToolOutlined /></div>
      </div>
    </div>

    <!-- 质检历史 -->
    <div class="table-container">
      <div class="table-header">
        <h4><HistoryOutlined style="color: var(--primary-color); margin-right: 8px" /> 质检历史记录</h4>
        <a-button>
          <template #icon><ExportOutlined /></template>
          导出报告
        </a-button>
      </div>
      <table class="data-table">
        <thead>
          <tr>
            <th>归还单号</th>
            <th>设备编号</th>
            <th>设备名称</th>
            <th>质检时间</th>
            <th>质检员</th>
            <th>质检结果</th>
            <th>维修费用</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in historyData" :key="item.key">
            <td>{{ item.return_code }}</td>
            <td>{{ item.equipment_code }}</td>
            <td>{{ item.equipment_name }}</td>
            <td>{{ item.inspection_date }}</td>
            <td>{{ item.inspector }}</td>
            <td>
              <span :class="item.result === '合格' ? 'badge badge-success' : 'badge badge-warning'">
                {{ item.result }}
              </span>
            </td>
            <td>{{ item.repair_cost }}</td>
            <td>
              <a @click="showReport(item)">查看报告</a>
            </td>
          </tr>
        </tbody>
      </table>
      <div style="margin-top: 15px; display: flex; justify-content: space-between; align-items: center">
        <span style="color: #666; font-size: 14px">显示 1-10 / 共 234 条</span>
        <a-pagination
          v-model:current="currentPage"
          :total="234"
          size="small"
        />
      </div>
    </div>
  </div>
</template>

    <!-- 质检模态框 -->
    <a-modal
      v-model:open="inspectionModalVisible"
      title="设备质检"
      width="800px"
      @ok="handleSubmitInspection"
    >
      <a-form
        :model="inspectionData"
        :label-col="{ span: 6 }"
        :wrapper-col="{ span: 16 }"
      >
        <a-form-item label="设备编号">
          <a-input v-model:value="inspectionData.equipment_code" disabled />
        </a-form-item>
        <a-form-item label="质检员">
          <a-input v-model:value="inspectionData.inspector" />
        </a-form-item>
        <a-form-item label="外观状况">
          <a-select v-model:value="inspectionData.appearance_status">
            <a-select-option value="完好">完好</a-select-option>
            <a-select-option value="轻微磨损">轻微磨损</a-select-option>
            <a-select-option value="严重损坏">严重损坏</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="功能测试">
          <a-radio-group v-model:value="inspectionData.function_test">
            <a-radio value="通过">通过</a-radio>
            <a-radio value="故障">故障</a-radio>
          </a-radio-group>
        </a-form-item>
        <a-form-item label="需要维修">
          <a-switch v-model:checked="needRepair" />
        </a-form-item>
        <a-form-item v-if="needRepair" label="维修费用">
          <a-input-number
            v-model:value="inspectionData.repair_cost"
            :min="0"
            :precision="2"
            style="width: 100%"
            prefix="¥"
          />
        </a-form-item>
        <a-form-item label="处理意见">
          <a-textarea v-model:value="inspectionData.remarks" :rows="4" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { message } from 'ant-design-vue'
import {
  CheckCircleOutlined,
  FilterOutlined,
  DatabaseOutlined,
  FileTextOutlined,
  InfoCircleOutlined,
  ClockCircleOutlined,
  LoadingOutlined,
  ToolOutlined,
  HistoryOutlined,
  ExportOutlined
} from '@ant-design/icons-vue'
import { createInspection } from '@/api'

const columns = [
  { title: '归还单号', dataIndex: 'return_code', key: 'return_code' },
  { title: '来源订单', dataIndex: 'order_code', key: 'order_code' },
  { title: '航次号', dataIndex: 'voyage_no', key: 'voyage_no' },
  { title: '设备数量', dataIndex: 'equipment_count', key: 'equipment_count' },
  { title: '归还时间', dataIndex: 'return_date', key: 'return_date' },
  { title: '状态', dataIndex: 'status', key: 'status' },
  { title: '操作', key: 'action' }
]

const mockData = ref([
  {
    key: '1',
    return_code: 'RET-0091',
    order_code: 'ORD-2023091501',
    voyage_no: 'V-9082',
    equipment_count: 3,
    return_date: '2023-10-25 10:30',
    status: '待质检'
  },
  {
    key: '2',
    return_code: 'RET-0088',
    order_code: 'ORD-2023091201',
    voyage_no: 'CH-7766',
    equipment_count: 7,
    return_date: '2023-10-24 14:20',
    status: '质检中'
  },
  {
    key: '3',
    return_code: 'RET-0085',
    order_code: 'ORD-2023090801',
    voyage_no: 'MSK-554',
    equipment_count: 5,
    return_date: '2023-10-23 09:15',
    status: '已入库'
  }
])

const historyData = ref([
  {
    key: '1',
    return_code: 'RET-0085',
    equipment_code: 'EQ-2023078',
    equipment_name: '防护栏板 (20米)',
    inspection_date: '2023-10-23 10:30',
    inspector: '张质检',
    result: '合格',
    repair_cost: '¥ 0.00'
  },
  {
    key: '2',
    return_code: 'RET-0083',
    equipment_code: 'FL-2002',
    equipment_name: '重油输送泵',
    inspection_date: '2023-10-22 14:20',
    inspector: '李质检',
    result: '需维修',
    repair_cost: '¥ 2,500.00'
  },
  {
    key: '3',
    return_code: 'RET-0080',
    equipment_code: 'HY-3305',
    equipment_name: '液压千斤顶 (50T)',
    inspection_date: '2023-10-21 09:15',
    inspector: '王质检',
    result: '合格',
    repair_cost: '¥ 0.00'
  }
])

const currentPage = ref(1)
const needRepair = ref(false)
const inspectionData = ref({
  return_id: null,
  equipment_id: null,
  equipment_code: '',
  inspector: '张质检',
  appearance_status: '完好',
  function_test: '通过',
  repair_needed: 0,
  repair_cost: 0,
  remarks: ''
})

const getStatusBadgeClass = (status) => {
  const classMap = {
    '待质检': 'badge badge-warning',
    '质检中': 'badge badge-info',
    '已入库': 'badge badge-success'
  }
  return classMap[status] || 'badge'
}

const showFilterModal = () => {
  message.info('筛选功能待完善')
}

const showEquipmentList = (record) => {
  message.info('设备清单功能待完善')
}

const continueInspection = (record) => {
  startInspection(record)
}

const showReport = (record) => {
  message.info('质检报告功能待完善')
}

const startInspection = (record) => {
  inspectionModalVisible.value = true
  inspectionData.value = {
    return_id: 1,
    equipment_id: 1,
    equipment_code: 'EQ-2023001',
    inspector: '张质检',
    appearance_status: '完好',
    function_test: '通过',
    repair_needed: 0,
    repair_cost: 0,
    remarks: ''
  }
}

const handleSubmitInspection = async () => {
  try {
    inspectionData.value.repair_needed = needRepair.value ? 1 : 0
    await createInspection(inspectionData.value)
    message.success('✓ 质检完成！\n- 设备状态已更新为：在库\n- 账单已自动生成（触发器：trg_auto_billing）\n- 库位已分配：A区-01-04')
  } catch (error) {
    message.error('质检提交失败')
  }
}
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


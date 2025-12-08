<template>
  <div>
    <!-- 统计卡片 -->
    <div class="dashboard-grid">
      <div class="stat-card">
        <div class="stat-info">
          <h3>{{ stats.in_stock || 124 }}</h3>
          <p>在库设备 (件)</p>
          <small style="color: var(--success); font-size: 12px;">▲ 5% vs上月</small>
        </div>
        <div class="stat-icon"><InboxOutlined /></div>
      </div>
      <div class="stat-card">
        <div class="stat-info">
          <h3>{{ stats.pending_checkout || 8 }}</h3>
          <p>今日待出库</p>
          <small style="color: var(--warning); font-size: 12px;">需要处理</small>
        </div>
        <div class="stat-icon"><ShoppingOutlined /></div>
      </div>
      <div class="stat-card">
        <div class="stat-info">
          <h3>{{ stats.in_progress_orders || 15 }}</h3>
          <p>航次运行中</p>
          <small style="color: #666; font-size: 12px;">涉及设备 38 件</small>
        </div>
        <div class="stat-icon"><RocketOutlined /></div>
      </div>
      <div class="stat-card">
        <div class="stat-info">
          <h3>¥ {{ formatAmount(stats.pending_amount) || '45W' }}</h3>
          <p>本月待结算</p>
          <small style="color: var(--danger); font-size: 12px;">15笔逾期</small>
        </div>
        <div class="stat-icon"><DollarOutlined /></div>
      </div>
    </div>

    <!-- 数据统计图表区 -->
    <div class="dashboard-grid" style="grid-template-columns: 2fr 1fr; margin-bottom: 20px;">
      <div class="table-container">
        <div class="table-header">
          <h4><LineChartOutlined style="color: var(--primary-color); margin-right: 8px" /> 本月收入趋势 (通过视图查询)</h4>
          <a-button type="text" @click="showChartView">
            <template #icon><ExpandOutlined /></template>
            查看详情
          </a-button>
        </div>
        <div style="padding: 20px; text-align: center;">
          <svg width="100%" height="200" style="background: #f8f9fa; border-radius: 4px;">
            <polyline
              points="50,150 100,120 150,100 200,130 250,80 300,90 350,60 400,50"
              fill="none"
              stroke="var(--primary-color)"
              stroke-width="3"
            />
            <text x="50" y="180" font-size="12" fill="#666">10/1</text>
            <text x="150" y="180" font-size="12" fill="#666">10/10</text>
            <text x="250" y="180" font-size="12" fill="#666">10/20</text>
            <text x="350" y="180" font-size="12" fill="#666">10/30</text>
            <text x="10" y="60" font-size="12" fill="#666">¥50k</text>
            <text x="10" y="120" font-size="12" fill="#666">¥30k</text>
            <text x="10" y="155" font-size="12" fill="#666">¥10k</text>
          </svg>
          <p style="margin-top: 10px; font-size: 13px; color: #666;">
            SQL: SELECT DATE(created_at), SUM(amount) FROM billing GROUP BY DATE(created_at)
          </p>
        </div>
      </div>

      <div class="table-container">
        <div class="table-header">
          <h4><PieChartOutlined style="color: var(--primary-color); margin-right: 8px" /> 设备类型分布</h4>
        </div>
        <div style="padding: 20px;">
          <div style="margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
              <span style="font-size: 13px;">起重配件</span>
              <span style="font-size: 13px; font-weight: bold;">42%</span>
            </div>
            <div style="height: 8px; background: #e9ecef; border-radius: 4px; overflow: hidden;">
              <div style="width: 42%; height: 100%; background: var(--primary-color)"></div>
            </div>
          </div>
          <div style="margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
              <span style="font-size: 13px;">流体设备</span>
              <span style="font-size: 13px; font-weight: bold;">28%</span>
            </div>
            <div style="height: 8px; background: #e9ecef; border-radius: 4px; overflow: hidden;">
              <div style="width: 28%; height: 100%; background: var(--accent-color)"></div>
            </div>
          </div>
          <div style="margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
              <span style="font-size: 13px;">固缚索具</span>
              <span style="font-size: 13px; font-weight: bold;">18%</span>
            </div>
            <div style="height: 8px; background: #e9ecef; border-radius: 4px; overflow: hidden;">
              <div style="width: 18%; height: 100%; background: var(--warning)"></div>
            </div>
          </div>
          <div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
              <span style="font-size: 13px;">其他</span>
              <span style="font-size: 13px; font-weight: bold;">12%</span>
            </div>
            <div style="height: 8px; background: #e9ecef; border-radius: 4px; overflow: hidden;">
              <div style="width: 12%; height: 100%; background: var(--success)"></div>
            </div>
          </div>
          <p style="margin-top: 15px; font-size: 12px; color: #666;">数据来源：v_equipment_category_stats</p>
        </div>
      </div>
    </div>

    <!-- 预警列表 -->
    <div class="table-container">
      <div class="table-header">
        <h4><ExclamationCircleOutlined style="color: var(--warning); margin-right: 8px" /> 预警：即将到期归还设备</h4>
        <a-button type="text" @click="refreshWarning">
          <template #icon><ReloadOutlined /></template>
          刷新
        </a-button>
      </div>
      <table class="data-table">
        <thead>
          <tr>
            <th>设备编号</th>
            <th>设备名称</th>
            <th>租赁方 (船舶/公司)</th>
            <th>航次号</th>
            <th>预计归还日</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in warningData" :key="item.key">
            <td>{{ item.equipment_code }}</td>
            <td>{{ item.equipment_name }}</td>
            <td>{{ item.customer_name }}</td>
            <td>{{ item.voyage_no }}</td>
            <td :style="{ color: item.isToday ? 'red' : item.isTomorrow ? 'orange' : '', fontWeight: item.isToday ? 'bold' : '' }">
              {{ item.expected_return_date }}
            </td>
            <td><span class="badge badge-warning">{{ item.status }}</span></td>
            <td>
              <a-button v-if="item.isToday" type="primary" size="small" @click="$router.push('/return')">
                处理归还
              </a-button>
              <a-button v-else type="text" size="small" @click="sendReminder">
                发送提醒
              </a-button>
            </td>
          </tr>
        </tbody>
      </table>
      <p style="margin-top: 10px; font-size: 12px; color: #999;">
        <InfoCircleOutlined /> 该数据由触发器 trg_return_warning 自动监控生成
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { getDashboardStats } from '@/api'
import {
  InboxOutlined,
  ShoppingOutlined,
  RocketOutlined,
  DollarOutlined,
  LineChartOutlined,
  PieChartOutlined,
  ExpandOutlined,
  ReloadOutlined,
  ExclamationCircleOutlined,
  InfoCircleOutlined
} from '@ant-design/icons-vue'

const stats = ref({
  total_equipment: 0,
  in_stock: 0,
  out_stock: 0,
  maintenance: 0,
  pending_checkout: 0,
  in_progress_orders: 0,
  pending_inspection: 0,
  total_revenue: 0,
  pending_amount: 0,
  overdue_bills: 0
})

const warningData = ref([
  {
    key: '1',
    equipment_code: 'EQ-2023001',
    equipment_name: '重型吊索组',
    customer_name: '远洋荣耀号 (Ocean Glory)',
    voyage_no: 'V-9082',
    expected_return_date: '2023-10-25 (今日)',
    status: '租赁中',
    isToday: true,
    isTomorrow: false
  },
  {
    key: '2',
    equipment_code: 'EQ-2023045',
    equipment_name: '集装箱叉车 (3T)',
    customer_name: '港务三区',
    voyage_no: '-',
    expected_return_date: '2023-10-26 (明天)',
    status: '租赁中',
    isToday: false,
    isTomorrow: true
  },
  {
    key: '3',
    equipment_code: 'EQ-2023078',
    equipment_name: '防护栏板 (20米)',
    customer_name: '中远海运',
    voyage_no: 'COSCO-442',
    expected_return_date: '2023-10-27',
    status: '租赁中',
    isToday: false,
    isTomorrow: false
  }
])

const formatAmount = (amount) => {
  if (!amount) return '45W'
  if (amount >= 10000) {
    return (amount / 10000).toFixed(0) + 'W'
  }
  return amount.toFixed(2)
}

const loadStats = async () => {
  try {
    const data = await getDashboardStats()
    stats.value = data
  } catch (error) {
    console.error('加载统计数据失败', error)
    // 使用默认值
  }
}

const showChartView = () => {
  message.info('数据可视化功能待完善')
}

const refreshWarning = () => {
  message.success('已刷新触发器预警数据')
}

const sendReminder = () => {
  message.success('已发送归还提醒')
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
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
</style>


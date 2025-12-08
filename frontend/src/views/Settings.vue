<template>
  <div>
    <div class="dashboard-grid" style="grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px">
      <!-- 数据库管理 -->
      <div class="table-container">
        <h4 style="margin-bottom: 15px; color: var(--primary-color)">
          <DatabaseOutlined style="margin-right: 8px" /> 数据库管理
        </h4>
        <div style="margin-bottom: 15px">
          <a-button type="primary" style="margin-right: 10px" @click="showViewManager">
            <template #icon><EyeOutlined /></template>
            视图管理
          </a-button>
          <a-button type="primary" style="margin-right: 10px" @click="showTriggerManager">
            <template #icon><ThunderboltOutlined /></template>
            触发器管理
          </a-button>
          <a-button @click="showProcedureManager">
            <template #icon><CodeOutlined /></template>
            存储过程
          </a-button>
        </div>
        <table class="data-table">
          <thead>
            <tr>
              <th>对象类型</th>
              <th>名称</th>
              <th>状态</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><span class="badge badge-info">视图</span></td>
              <td>v_equipment_status</td>
              <td><span class="badge badge-success">活动</span></td>
              <td>
                <a @click="showViewDetail" style="margin-right: 8px">查看</a>
                <a>编辑</a>
              </td>
            </tr>
            <tr>
              <td><span class="badge badge-warning">触发器</span></td>
              <td>trg_update_inventory</td>
              <td><span class="badge badge-success">活动</span></td>
              <td>
                <a @click="showTriggerDetail" style="margin-right: 8px">查看</a>
                <a>编辑</a>
              </td>
            </tr>
            <tr>
              <td><span class="badge badge-info">视图</span></td>
              <td>v_financial_report</td>
              <td><span class="badge badge-success">活动</span></td>
              <td>
                <a @click="showViewDetail" style="margin-right: 8px">查看</a>
                <a>编辑</a>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 用户权限管理 -->
      <div class="table-container">
        <h4 style="margin-bottom: 15px; color: var(--primary-color)">
          <UserOutlined style="margin-right: 8px" /> 用户权限管理
        </h4>
        <div style="margin-bottom: 15px">
          <a-button type="primary" style="margin-right: 10px" @click="showAddUser">
            <template #icon><UserAddOutlined /></template>
            添加用户
          </a-button>
          <a-button @click="showRoleManager">
            <template #icon><SafetyOutlined /></template>
            角色配置
          </a-button>
        </div>
        <table class="data-table">
          <thead>
            <tr>
              <th>用户名</th>
              <th>角色</th>
              <th>状态</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>张工</td>
              <td><span class="badge badge-danger">管理员</span></td>
              <td><span class="badge badge-success">在线</span></td>
              <td>
                <a @click="showUserDetail" style="margin-right: 8px">详情</a>
                <a>编辑</a>
              </td>
            </tr>
            <tr>
              <td>李仓管</td>
              <td><span class="badge badge-info">仓库管理</span></td>
              <td><span class="badge badge-success">在线</span></td>
              <td>
                <a @click="showUserDetail" style="margin-right: 8px">详情</a>
                <a>编辑</a>
              </td>
            </tr>
            <tr>
              <td>王财务</td>
              <td><span class="badge badge-warning">财务</span></td>
              <td><span style="color: #999">离线</span></td>
              <td>
                <a @click="showUserDetail" style="margin-right: 8px">详情</a>
                <a>编辑</a>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 系统日志 -->
      <div class="table-container">
        <h4 style="margin-bottom: 15px; color: var(--primary-color)">
          <FileTextOutlined style="margin-right: 8px" /> 系统操作日志
        </h4>
        <div style="margin-bottom: 15px">
          <a-button style="margin-right: 10px" @click="showLogFilter">
            <template #icon><FilterOutlined /></template>
            筛选日志
          </a-button>
          <a-button>
            <template #icon><DownloadOutlined /></template>
            导出日志
          </a-button>
        </div>
        <table class="data-table">
          <thead>
            <tr>
              <th>时间</th>
              <th>操作员</th>
              <th>操作类型</th>
              <th>描述</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in logData" :key="item.key">
              <td>{{ item.created_at }}</td>
              <td>{{ item.username }}</td>
              <td><span :class="getActionBadgeClass(item.action)">{{ item.action }}</span></td>
              <td>{{ item.description }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 数据统计 -->
      <div class="table-container">
        <h4 style="margin-bottom: 15px; color: var(--primary-color)">
          <BarChartOutlined style="margin-right: 8px" /> 数据统计与报表
        </h4>
        <div style="margin-bottom: 15px">
          <a-button type="primary" style="margin-right: 10px" @click="showReportConfig">
            <template #icon><PieChartOutlined /></template>
            生成报表
          </a-button>
          <a-button style="margin-right: 10px" @click="showChartView">
            <template #icon><LineChartOutlined /></template>
            数据可视化
          </a-button>
          <a-button @click="showDatabaseInfo">
            <template #icon><DatabaseOutlined /></template>
            查看数据库架构
          </a-button>
        </div>
        <div style="padding: 20px; background: #f8f9fa; border-radius: 4px">
          <p style="margin-bottom: 10px"><strong>数据库连接查询示例：</strong></p>
          <ul style="list-style: none; padding-left: 0; font-size: 13px; color: #666">
            <li style="margin-bottom: 8px">✓ 设备-租赁订单关联查询 (JOIN 3张表)</li>
            <li style="margin-bottom: 8px">✓ 客户-账单-付款记录多表联查 (LEFT JOIN)</li>
            <li style="margin-bottom: 8px">✓ 库存统计聚合视图 (GROUP BY + COUNT)</li>
            <li style="margin-bottom: 8px">✓ 设备使用频率分析 (子查询 + 排序)</li>
            <li style="margin-bottom: 8px">✓ 收入趋势时间序列查询 (DATE函数 + SUM)</li>
            <li style="margin-bottom: 8px">✓ 库存预警自动触发 (触发器 + 条件判断)</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- 数据库架构展示 -->
    <div class="table-container" style="margin-top: 20px">
      <div class="table-header">
        <h4><ProjectOutlined style="color: var(--primary-color); margin-right: 8px" /> 核心数据库表结构一览</h4>
        <a-button @click="showDatabaseInfo">
          <template #icon><ExpandOutlined /></template>
          查看完整ER图
        </a-button>
      </div>
      <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; padding: 15px 0">
        <div style="padding: 15px; background: #f8f9fa; border-left: 4px solid var(--primary-color); border-radius: 4px">
          <h5 style="margin-bottom: 10px; color: var(--primary-color)">
            <TableOutlined style="margin-right: 8px" /> equipment (设备表)
          </h5>
          <ul style="font-size: 12px; color: #666; list-style: none; padding: 0">
            <li>• equipment_id (PK)</li>
            <li>• equipment_name</li>
            <li>• category</li>
            <li>• status</li>
            <li>• storage_location</li>
            <li>• created_at</li>
          </ul>
        </div>
        <div style="padding: 15px; background: #f8f9fa; border-left: 4px solid var(--accent-color); border-radius: 4px">
          <h5 style="margin-bottom: 10px; color: var(--accent-color)">
            <TableOutlined style="margin-right: 8px" /> lease_orders (租赁订单)
          </h5>
          <ul style="font-size: 12px; color: #666; list-style: none; padding: 0">
            <li>• order_id (PK)</li>
            <li>• customer_name</li>
            <li>• voyage_no</li>
            <li>• start_date</li>
            <li>• return_date</li>
            <li>• status</li>
          </ul>
        </div>
        <div style="padding: 15px; background: #f8f9fa; border-left: 4px solid var(--warning); border-radius: 4px">
          <h5 style="margin-bottom: 10px; color: var(--warning)">
            <TableOutlined style="margin-right: 8px" /> billing (账单表)
          </h5>
          <ul style="font-size: 12px; color: #666; list-style: none; padding: 0">
            <li>• bill_id (PK)</li>
            <li>• order_id (FK)</li>
            <li>• customer_name</li>
            <li>• amount</li>
            <li>• repair_fee</li>
            <li>• status</li>
          </ul>
        </div>
        <div style="padding: 15px; background: #f8f9fa; border-left: 4px solid var(--success); border-radius: 4px">
          <h5 style="margin-bottom: 10px; color: var(--success)">
            <TableOutlined style="margin-right: 8px" /> order_items (订单明细)
          </h5>
          <ul style="font-size: 12px; color: #666; list-style: none; padding: 0">
            <li>• item_id (PK)</li>
            <li>• order_id (FK)</li>
            <li>• equipment_id (FK)</li>
            <li>• daily_rate</li>
            <li>• days</li>
          </ul>
        </div>
        <div style="padding: 15px; background: #f8f9fa; border-left: 4px solid var(--danger); border-radius: 4px">
          <h5 style="margin-bottom: 10px; color: var(--danger)">
            <TableOutlined style="margin-right: 8px" /> inspection_records (质检)
          </h5>
          <ul style="font-size: 12px; color: #666; list-style: none; padding: 0">
            <li>• inspection_id (PK)</li>
            <li>• equipment_id (FK)</li>
            <li>• inspector</li>
            <li>• appearance</li>
            <li>• function_test</li>
            <li>• result</li>
          </ul>
        </div>
        <div style="padding: 15px; background: #f8f9fa; border-left: 4px solid #6c757d; border-radius: 4px">
          <h5 style="margin-bottom: 10px; color: #6c757d">
            <TableOutlined style="margin-right: 8px" /> operation_logs (日志)
          </h5>
          <ul style="font-size: 12px; color: #666; list-style: none; padding: 0">
            <li>• log_id (PK)</li>
            <li>• user_id</li>
            <li>• action</li>
            <li>• description</li>
            <li>• created_at</li>
          </ul>
        </div>
      </div>
      <p style="margin-top: 10px; padding: 10px; background: #e7f3ff; border-radius: 4px; font-size: 13px">
        <InfoCircleOutlined /> <strong>数据库关系：</strong>
        equipment ←→ order_items ←→ lease_orders ←→ billing |
        equipment → inspection_records |
        所有表 → operation_logs (日志记录)
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { message } from 'ant-design-vue'
import {
  DatabaseOutlined,
  EyeOutlined,
  ThunderboltOutlined,
  CodeOutlined,
  UserOutlined,
  UserAddOutlined,
  SafetyOutlined,
  FileTextOutlined,
  FilterOutlined,
  DownloadOutlined,
  BarChartOutlined,
  PieChartOutlined,
  LineChartOutlined,
  ProjectOutlined,
  ExpandOutlined,
  TableOutlined,
  InfoCircleOutlined
} from '@ant-design/icons-vue'

const logData = ref([
  {
    key: '1',
    created_at: '2023-10-25 14:32',
    username: '张工',
    action: '新增',
    description: '创建租赁订单 ORD-2023102401'
  },
  {
    key: '2',
    created_at: '2023-10-25 14:15',
    username: '李仓管',
    action: '修改',
    description: '更新设备状态 EQ-2023001'
  },
  {
    key: '3',
    created_at: '2023-10-25 13:58',
    username: '王财务',
    action: '查询',
    description: '导出月度财务报表'
  }
])

const getActionBadgeClass = (action) => {
  const classMap = {
    '新增': 'badge badge-info',
    '修改': 'badge badge-warning',
    '删除': 'badge badge-danger',
    '查询': 'badge badge-success'
  }
  return classMap[action] || 'badge'
}

const showDatabaseInfo = () => {
  message.info('数据库架构功能待完善')
}

const showViewManager = () => {
  message.info('视图管理功能待完善')
}

const showTriggerManager = () => {
  message.info('触发器管理功能待完善')
}

const showProcedureManager = () => {
  message.info('存储过程管理功能待完善')
}

const showViewDetail = () => {
  message.info('视图详情功能待完善')
}

const showTriggerDetail = () => {
  message.info('触发器详情功能待完善')
}

const showAddUser = () => {
  message.info('添加用户功能待完善')
}

const showRoleManager = () => {
  message.info('角色配置功能待完善')
}

const showUserDetail = () => {
  message.info('用户详情功能待完善')
}

const showLogFilter = () => {
  message.info('日志筛选功能待完善')
}

const showReportConfig = () => {
  message.info('报表配置功能待完善')
}

const showChartView = () => {
  message.info('数据可视化功能待完善')
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

.data-table ul {
  margin: 0;
}
</style>


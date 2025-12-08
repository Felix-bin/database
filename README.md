# 船舶作业装备租赁与港口仓储管理系统

## 项目简介

基于 Vue 3 + Ant Design Vue + FastAPI + OceanBase/MySQL 构建的现代化船舶作业装备租赁与港口仓储管理系统。

### 技术栈

**前端：**
- Vue 3 (Composition API)
- Ant Design Vue 4.x
- Vue Router 4
- Pinia (状态管理)
- Axios (HTTP 客户端)
- Vite (构建工具)

**后端：**
- FastAPI (Python Web 框架)
- SQLAlchemy (ORM)
- Pydantic (数据验证)
- OceanBase / MySQL (数据库)
- Uvicorn (ASGI 服务器)

### 核心功能

1. **工作台概览** - 数据统计、预警提醒、快速操作
2. **仓储与库存** - 设备管理、库位分配、批量操作
3. **租赁与出库** - 订单创建、设备选配、出库办理
4. **归还与质检** - 质检录入、状态更新、维修记录
5. **费用结算** - 账单管理、费用明细、报表导出
6. **系统设置** - 数据库管理、用户权限、操作日志

### 数据库设计

#### 核心表结构
- `equipment` - 设备表
- `lease_orders` - 租赁订单表
- `order_items` - 订单明细表
- `billing` - 账单表
- `customers` - 客户表
- `return_records` - 归还记录表
- `inspection_records` - 质检记录表
- `users` - 用户表
- `operation_logs` - 操作日志表

#### 数据库特性
- **视图** - 设备状态视图、财务报表视图、订单详情视图等
- **触发器** - 自动更新库存、自动生成账单、记录操作日志
- **存储过程** - 费用计算、批量状态更新、报表生成
- **连接查询** - 多表 JOIN、聚合查询、时间序列分析

## 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- OceanBase / MySQL 5.7+

### 安装步骤

#### 1. 克隆项目

```bash
git clone <repository-url>
cd test
```

#### 2. 后端设置

```bash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置数据库
# 修改 database.py 中的数据库连接信息：
# DB_USER = 'root@mysql001'
# DB_PASSWORD = 'MySql123456.@'
# DB_HOST = '127.0.0.1'
# DB_PORT = 2881
# DB_NAME = 'port_equipment_db'

# 初始化数据库
python init_db.py

# 启动后端服务
python main.py
# 或使用 uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

后端服务将在 http://localhost:8000 启动
API 文档地址：http://localhost:8000/docs

#### 3. 前端设置

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务将在 http://localhost:5173 启动

### 默认账户

初始化数据库后，将创建以下默认账户：

- 管理员：`admin` / `admin123`
- 操作员：`zhanggong` / `123456`

## 项目结构

```
test/
├── backend/                # 后端代码
│   ├── main.py            # FastAPI 主应用
│   ├── database.py        # 数据库连接配置
│   ├── models.py          # SQLAlchemy 数据模型
│   ├── schemas.py         # Pydantic 数据验证模型
│   ├── crud.py            # CRUD 操作函数
│   ├── init_db.py         # 数据库初始化脚本
│   └── requirements.txt   # Python 依赖
│
├── frontend/              # 前端代码
│   ├── src/
│   │   ├── views/         # 页面组件
│   │   │   ├── Layout.vue
│   │   │   ├── Dashboard.vue
│   │   │   ├── Inventory.vue
│   │   │   ├── Leasing.vue
│   │   │   ├── Finance.vue
│   │   │   ├── Return.vue
│   │   │   └── Settings.vue
│   │   ├── router/        # 路由配置
│   │   ├── stores/        # Pinia 状态管理
│   │   ├── api/           # API 接口封装
│   │   ├── App.vue
│   │   ├── main.js
│   │   └── style.css
│   ├── index.html
│   ├── vite.config.js     # Vite 配置
│   └── package.json       # Node.js 依赖
│
├── test.html              # 原型图
└── README.md              # 项目文档
```

## API 接口

### 工作台
- `GET /api/dashboard/stats` - 获取统计数据

### 设备管理
- `GET /api/equipment` - 获取设备列表
- `GET /api/equipment/{id}` - 获取设备详情
- `POST /api/equipment` - 创建设备
- `PUT /api/equipment/{id}` - 更新设备
- `DELETE /api/equipment/{id}` - 删除设备

### 客户管理
- `GET /api/customers` - 获取客户列表
- `POST /api/customers` - 创建客户

### 订单管理
- `GET /api/orders` - 获取订单列表
- `GET /api/orders/{id}` - 获取订单详情
- `POST /api/orders` - 创建订单
- `PUT /api/orders/{id}` - 更新订单

### 账单管理
- `GET /api/billing` - 获取账单列表
- `POST /api/billing` - 创建账单
- `PUT /api/billing/{id}` - 更新账单

### 归还与质检
- `POST /api/returns` - 创建归还记录
- `POST /api/inspections` - 创建质检记录

完整 API 文档请访问：http://localhost:8000/docs

## 开发说明

### 数据库连接

参考 `main.py` 中的数据库连接示例：

```python
from urllib.parse import quote_plus
from sqlalchemy import create_engine

DB_USER = 'root@mysql001'
DB_PASSWORD = 'MySql123456.@'
DB_HOST = '127.0.0.1'
DB_PORT = 2881
DB_NAME = 'port_equipment_db'

encoded_user = quote_plus(DB_USER)
encoded_password = quote_plus(DB_PASSWORD)

DATABASE_URL = f"mysql+mysqldb://{encoded_user}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
```

### 添加新功能

1. **后端：**
   - 在 `models.py` 中定义数据模型
   - 在 `schemas.py` 中定义 Pydantic 模型
   - 在 `crud.py` 中实现 CRUD 操作
   - 在 `main.py` 中添加路由

2. **前端：**
   - 在 `src/views/` 中创建页面组件
   - 在 `src/router/index.js` 中添加路由
   - 在 `src/api/index.js` 中添加 API 接口

### 部署

#### 后端部署

```bash
# 使用 Gunicorn + Uvicorn
pip install gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### 前端部署

```bash
# 构建生产版本
npm run build

# dist 目录可部署到 Nginx 或其他静态服务器
```

## 常见问题

### 数据库连接失败

1. 确认数据库服务已启动
2. 检查 `database.py` 中的连接参数
3. 确认数据库用户权限

### 前端无法访问后端 API

1. 确认后端服务已启动（http://localhost:8000）
2. 检查 `vite.config.js` 中的代理配置
3. 检查浏览器控制台的 CORS 错误

## 许可证

MIT License

## 联系方式

如有问题，请联系开发团队。


# 安装和运行指南

## 快速开始（推荐）

### 方式一：使用一键启动脚本

```bash
# 给脚本添加执行权限
chmod +x start.sh

# 运行启动脚本
./start.sh
```

脚本会自动完成以下步骤：
1. 检查 Python 环境
2. 创建数据库（首次运行时选择）
3. 初始化数据表和初始数据
4. 启动后端服务 (http://localhost:8000)
5. 启动前端服务 (http://localhost:5173)

---

## 手动安装步骤

### 环境要求

- **Python**: 3.8+
- **Node.js**: 16+
- **OceanBase/MySQL**: 5.7+

### 第一步：安装后端

```bash
cd backend

# 安装依赖（推荐使用 uv）
pip install uv
uv pip install -r pyproject.toml

# 或使用传统方式
pip install fastapi uvicorn sqlalchemy mysqlclient pydantic python-multipart

# 配置数据库连接
# 编辑 backend/database.py 文件，修改以下参数：
# DB_USER = 'root@mysql001'
# DB_PASSWORD = 'MySql123456.@'
# DB_HOST = '127.0.0.1'
# DB_PORT = 2881
# DB_NAME = 'port_equipment_db'
```

### 第二步：初始化数据库

```bash
# 创建数据库
python create_database.py

# 初始化表结构和数据
python init_db.py
```

成功后会显示：
```
✓ 数据库 'port_equipment_db' 创建成功！
正在创建数据库表...
数据库表创建完成！
正在插入初始数据...
初始数据插入完成！

默认账户信息：
管理员 - 用户名: admin, 密码: admin123
操作员 - 用户名: zhanggong, 密码: 123456
```

### 第三步：启动后端服务

```bash
# 方式1：直接运行
python main.py

# 方式2：使用 uvicorn（推荐）
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 方式3：使用 uv
uv run main.py
```

后端服务地址：
- API: http://localhost:8000
- 交互式文档: http://localhost:8000/docs
- ReDoc 文档: http://localhost:8000/redoc

### 第四步：安装前端

```bash
cd ../frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务地址：http://localhost:5173

---

## 验证安装

### 1. 检查后端

访问 http://localhost:8000/health

应该返回：
```json
{
  "status": "healthy",
  "service": "Port Equipment Management System"
}
```

### 2. 检查前端

访问 http://localhost:5173

应该看到登录界面或系统主页

### 3. 测试 API

```bash
# 获取统计数据
curl http://localhost:8000/api/dashboard/stats

# 获取设备列表
curl http://localhost:8000/api/equipment?page=1&page_size=10
```

---

## 常见问题

### Q1: 数据库连接失败

**错误**: `sqlalchemy.exc.OperationalError: (1049, "Unknown database 'port_equipment_db'")`

**解决**:
1. 确认 OceanBase/MySQL 服务已启动
2. 运行 `python create_database.py` 创建数据库
3. 检查 `database.py` 中的连接参数是否正确

### Q2: bcrypt 版本错误

**错误**: `AttributeError: module 'bcrypt' has no attribute '__about__'`

**解决**:
本项目已改用 SHA256 哈希，无需 bcrypt。如果仍有错误，请删除 `.venv` 重新安装依赖。

### Q3: 前端无法访问后端

**错误**: 前端显示网络错误或 CORS 错误

**解决**:
1. 确认后端服务已启动 (http://localhost:8000)
2. 检查 `frontend/vite.config.js` 中的代理配置
3. 检查浏览器控制台是否有 CORS 错误

### Q4: 端口被占用

**错误**: `Address already in use`

**解决**:
```bash
# 查找占用端口的进程
# 后端端口 8000
lsof -i :8000
# 或
netstat -tulnp | grep 8000

# 前端端口 5173
lsof -i :5173

# 杀死进程
kill -9 <PID>
```

### Q5: Node.js 依赖安装失败

**解决**:
```bash
# 清除缓存
npm cache clean --force

# 删除 node_modules 重新安装
rm -rf node_modules package-lock.json
npm install

# 或使用淘宝镜像
npm install --registry=https://registry.npmmirror.com
```

---

## 生产部署

### 后端部署

```bash
# 使用 Gunicorn + Uvicorn Workers
pip install gunicorn
gunicorn main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --access-logfile access.log \
    --error-logfile error.log
```

### 前端部署

```bash
cd frontend

# 构建生产版本
npm run build

# dist 目录可部署到 Nginx
```

Nginx 配置示例：
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # 前端静态文件
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
    
    # 后端 API 代理
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                     用户浏览器                           │
│              http://localhost:5173                      │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│              前端 (Vue 3 + Ant Design)                   │
│  - 页面组件 (Dashboard, Inventory, etc.)                 │
│  - 路由管理 (Vue Router)                                 │
│  - 状态管理 (Pinia)                                      │
│  - API 调用 (Axios)                                      │
└─────────────────┬───────────────────────────────────────┘
                  │ HTTP/REST API
                  ▼
┌─────────────────────────────────────────────────────────┐
│              后端 (FastAPI)                              │
│  - RESTful API (main.py)                                │
│  - 业务逻辑 (crud.py)                                    │
│  - 数据验证 (schemas.py)                                 │
│  - ORM 模型 (models.py)                                  │
└─────────────────┬───────────────────────────────────────┘
                  │ SQLAlchemy ORM
                  ▼
┌─────────────────────────────────────────────────────────┐
│           数据库 (OceanBase/MySQL)                       │
│  - 9张核心业务表                                          │
│  - 视图、触发器、存储过程                                 │
│  - 索引优化                                              │
└─────────────────────────────────────────────────────────┘
```

---

## 开发建议

### 代码规范

- Python: 遵循 PEP 8
- JavaScript: 遵循 ESLint 规则
- 提交前运行代码检查

### 调试技巧

**后端调试**:
```bash
# 启用 SQL 日志
# 在 database.py 中设置 echo=True
engine = create_engine(DATABASE_URL, echo=True)

# 使用 FastAPI 自带调试
uvicorn main:app --reload --log-level debug
```

**前端调试**:
```bash
# 使用 Vue Devtools
# 检查浏览器控制台
# 使用 Vite 的 HMR 功能
```

---

## 技术支持

如遇问题，请检查：
1. 日志文件
2. 数据库连接
3. 端口占用情况
4. 依赖版本兼容性

更多信息请查看 `README.md`


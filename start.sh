#!/bin/bash

echo "=========================================="
echo "船舶作业装备租赁与港口仓储管理系统"
echo "=========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查 Python 环境
echo -e "${YELLOW}检查 Python 环境...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}错误: 未找到 Python3${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python 环境正常${NC}"
echo ""

# 询问是否需要初始化数据库
echo -e "${YELLOW}是否需要初始化数据库？${NC}"
echo "1) 是 - 创建数据库并初始化表和数据"
echo "2) 否 - 跳过数据库初始化"
read -p "请选择 (1/2): " db_choice

if [ "$db_choice" = "1" ]; then
    echo ""
    echo -e "${YELLOW}步骤 1: 创建数据库${NC}"
    cd backend
    python3 create_database.py
    
    if [ $? -eq 0 ]; then
        echo ""
        echo -e "${YELLOW}步骤 2: 初始化数据库表和数据${NC}"
        python3 init_db.py
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ 数据库初始化成功${NC}"
        else
            echo -e "${RED}✗ 数据库初始化失败${NC}"
            exit 1
        fi
    else
        echo -e "${RED}✗ 数据库创建失败${NC}"
        exit 1
    fi
    cd ..
fi

echo ""
echo -e "${YELLOW}步骤 3: 启动后端服务${NC}"
echo "后端服务将在 http://localhost:8000 启动"
echo "API 文档地址: http://localhost:8000/docs"
echo ""

cd backend
python3 main.py &
BACKEND_PID=$!
cd ..

echo -e "${GREEN}✓ 后端服务已启动 (PID: $BACKEND_PID)${NC}"
echo ""

# 等待后端启动
sleep 3

echo -e "${YELLOW}步骤 4: 启动前端服务${NC}"
echo "前端服务将在 http://localhost:5173 启动"
echo ""

cd frontend

# 检查是否已安装依赖
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}首次运行，正在安装前端依赖...${NC}"
    npm install
fi

npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo -e "${GREEN}✓ 前端服务已启动 (PID: $FRONTEND_PID)${NC}"
echo ""
echo "=========================================="
echo -e "${GREEN}系统启动完成！${NC}"
echo "=========================================="
echo ""
echo "访问地址："
echo "  前端: http://localhost:5173"
echo "  后端: http://localhost:8000"
echo "  API文档: http://localhost:8000/docs"
echo ""
echo "默认账户："
echo "  管理员: admin / admin123"
echo "  操作员: zhanggong / 123456"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

# 等待用户中断
wait


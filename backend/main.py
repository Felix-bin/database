from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional, List
import crud
import models
import schemas
from database import engine, get_db

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

# 创建 FastAPI 应用
app = FastAPI(
    title="船舶作业装备租赁与港口仓储管理系统 API",
    description="Port Equipment Management System API",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:5173", "http://127.0.0.1:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========== 根路由 ==========
@app.get("/")
def read_root():
    return {
        "message": "欢迎使用船舶作业装备租赁与港口仓储管理系统 API",
        "version": "1.0.0",
        "docs": "/docs"
    }


# ========== 工作台统计 ==========
@app.get("/api/dashboard/stats", response_model=schemas.DashboardStats, tags=["Dashboard"])
def get_dashboard_stats(db: Session = Depends(get_db)):
    """获取工作台统计数据"""
    return crud.get_dashboard_stats(db)


# ========== 设备管理 API ==========
@app.get("/api/equipment", response_model=schemas.PageResponse, tags=["Equipment"])
def list_equipment(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: Optional[str] = None,
    category: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取设备列表"""
    skip = (page - 1) * page_size
    result = crud.get_equipment_list(
        db, skip=skip, limit=page_size,
        keyword=keyword, category=category, status=status
    )
    
    return schemas.PageResponse(
        data=[schemas.Equipment.from_orm(item) for item in result["items"]],
        total=result["total"],
        page=page,
        page_size=page_size
    )


@app.get("/api/equipment/{equipment_id}", response_model=schemas.Equipment, tags=["Equipment"])
def get_equipment(equipment_id: int, db: Session = Depends(get_db)):
    """获取设备详情"""
    equipment = crud.get_equipment_by_id(db, equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="设备不存在")
    return equipment


@app.post("/api/equipment", response_model=schemas.Equipment, tags=["Equipment"])
def create_equipment(equipment: schemas.EquipmentCreate, db: Session = Depends(get_db)):
    """创建设备"""
    return crud.create_equipment(db, equipment)


@app.put("/api/equipment/{equipment_id}", response_model=schemas.Equipment, tags=["Equipment"])
def update_equipment(
    equipment_id: int,
    equipment: schemas.EquipmentUpdate,
    db: Session = Depends(get_db)
):
    """更新设备"""
    updated = crud.update_equipment(db, equipment_id, equipment)
    if not updated:
        raise HTTPException(status_code=404, detail="设备不存在")
    return updated


@app.delete("/api/equipment/{equipment_id}", tags=["Equipment"])
def delete_equipment(equipment_id: int, db: Session = Depends(get_db)):
    """删除设备"""
    deleted = crud.delete_equipment(db, equipment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="设备不存在")
    return schemas.Response(message="删除成功")


# ========== 客户管理 API ==========
@app.get("/api/customers", response_model=schemas.PageResponse, tags=["Customer"])
def list_customers(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取客户列表"""
    skip = (page - 1) * page_size
    result = crud.get_customer_list(db, skip=skip, limit=page_size, keyword=keyword)
    
    return schemas.PageResponse(
        data=[schemas.Customer.from_orm(item) for item in result["items"]],
        total=result["total"],
        page=page,
        page_size=page_size
    )


@app.post("/api/customers", response_model=schemas.Customer, tags=["Customer"])
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    """创建客户"""
    return crud.create_customer(db, customer)


# ========== 租赁订单 API ==========
@app.get("/api/orders", response_model=schemas.PageResponse, tags=["Order"])
def list_orders(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,
    keyword: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取订单列表"""
    skip = (page - 1) * page_size
    result = crud.get_order_list(
        db, skip=skip, limit=page_size,
        status=status, keyword=keyword
    )
    
    return schemas.PageResponse(
        data=[schemas.LeaseOrder.from_orm(item) for item in result["items"]],
        total=result["total"],
        page=page,
        page_size=page_size
    )


@app.get("/api/orders/{order_id}", response_model=schemas.LeaseOrder, tags=["Order"])
def get_order(order_id: int, db: Session = Depends(get_db)):
    """获取订单详情"""
    order = crud.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    return order


@app.post("/api/orders", response_model=schemas.LeaseOrder, tags=["Order"])
def create_order(order: schemas.LeaseOrderCreate, db: Session = Depends(get_db)):
    """创建租赁订单"""
    return crud.create_order(db, order)


@app.put("/api/orders/{order_id}", response_model=schemas.LeaseOrder, tags=["Order"])
def update_order(
    order_id: int,
    order: schemas.LeaseOrderUpdate,
    db: Session = Depends(get_db)
):
    """更新订单"""
    updated = crud.update_order(db, order_id, order)
    if not updated:
        raise HTTPException(status_code=404, detail="订单不存在")
    return updated


# ========== 账单管理 API ==========
@app.get("/api/billing", response_model=schemas.PageResponse, tags=["Billing"])
def list_billing(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,
    keyword: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取账单列表"""
    skip = (page - 1) * page_size
    result = crud.get_billing_list(
        db, skip=skip, limit=page_size,
        status=status, keyword=keyword
    )
    
    return schemas.PageResponse(
        data=[schemas.Billing.from_orm(item) for item in result["items"]],
        total=result["total"],
        page=page,
        page_size=page_size
    )


@app.post("/api/billing", response_model=schemas.Billing, tags=["Billing"])
def create_billing(billing: schemas.BillingCreate, db: Session = Depends(get_db)):
    """创建账单"""
    return crud.create_billing(db, billing)


@app.put("/api/billing/{bill_id}", response_model=schemas.Billing, tags=["Billing"])
def update_billing(
    bill_id: int,
    billing: schemas.BillingUpdate,
    db: Session = Depends(get_db)
):
    """更新账单"""
    updated = crud.update_billing(db, bill_id, billing)
    if not updated:
        raise HTTPException(status_code=404, detail="账单不存在")
    return updated


# ========== 归还与质检 API ==========
@app.post("/api/returns", response_model=schemas.ReturnRecord, tags=["Return"])
def create_return(return_record: schemas.ReturnRecordCreate, db: Session = Depends(get_db)):
    """创建归还记录"""
    return crud.create_return_record(db, return_record)


@app.post("/api/inspections", response_model=schemas.InspectionRecord, tags=["Inspection"])
def create_inspection(inspection: schemas.InspectionRecordCreate, db: Session = Depends(get_db)):
    """创建质检记录"""
    return crud.create_inspection_record(db, inspection)


# ========== 认证 API ==========
@app.post("/api/auth/login", response_model=schemas.LoginResponse, tags=["Auth"])
def login(login_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    """用户登录"""
    user = crud.authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    return schemas.LoginResponse(
        code=200,
        message="登录成功",
        data={
            "user_id": user.user_id,
            "username": user.username,
            "real_name": user.real_name,
            "role": user.role,
            "email": user.email,
            "phone": user.phone
        }
    )


@app.post("/api/auth/register", response_model=schemas.RegisterResponse, tags=["Auth"])
def register(register_data: schemas.RegisterRequest, db: Session = Depends(get_db)):
    """用户注册"""
    # 检查用户名是否已存在
    existing_user = crud.get_user_by_username(db, register_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    # 创建用户
    user_create = schemas.UserCreate(
        username=register_data.username,
        password=register_data.password,
        real_name=register_data.real_name,
        email=register_data.email,
        phone=register_data.phone,
        role="operator"  # 默认角色为操作员
    )
    
    user = crud.create_user(db, user_create)
    
    return schemas.RegisterResponse(
        code=200,
        message="注册成功",
        data={
            "user_id": user.user_id,
            "username": user.username,
            "real_name": user.real_name,
            "email": user.email,
            "phone": user.phone
        }
    )


# ========== 健康检查 ==========
@app.get("/health", tags=["System"])
def health_check():
    """健康检查"""
    return {"status": "healthy", "service": "Port Equipment Management System"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional
from datetime import datetime, date
import models
import schemas
import hashlib

def hash_password(password: str) -> str:
    """使用 SHA256 哈希密码"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return hash_password(plain_password) == hashed_password


# ========== 设备管理 CRUD ==========
def get_equipment_list(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    keyword: Optional[str] = None,
    category: Optional[str] = None,
    status: Optional[str] = None
):
    """获取设备列表"""
    query = db.query(models.Equipment).filter(models.Equipment.is_deleted == 0)
    
    if keyword:
        query = query.filter(
            or_(
                models.Equipment.equipment_code.contains(keyword),
                models.Equipment.equipment_name.contains(keyword)
            )
        )
    if category:
        query = query.filter(models.Equipment.category == category)
    if status:
        query = query.filter(models.Equipment.status == status)
    
    total = query.count()
    items = query.order_by(models.Equipment.created_at.desc()).offset(skip).limit(limit).all()
    
    return {"total": total, "items": items}


def get_equipment_by_id(db: Session, equipment_id: int):
    """根据ID获取设备"""
    return db.query(models.Equipment).filter(
        models.Equipment.equipment_id == equipment_id,
        models.Equipment.is_deleted == 0
    ).first()


def create_equipment(db: Session, equipment: schemas.EquipmentCreate):
    """创建设备"""
    db_equipment = models.Equipment(**equipment.dict())
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    return db_equipment


def update_equipment(db: Session, equipment_id: int, equipment: schemas.EquipmentUpdate):
    """更新设备"""
    db_equipment = get_equipment_by_id(db, equipment_id)
    if not db_equipment:
        return None
    
    update_data = equipment.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_equipment, key, value)
    
    db.commit()
    db.refresh(db_equipment)
    return db_equipment


def delete_equipment(db: Session, equipment_id: int):
    """删除设备（软删除）"""
    db_equipment = get_equipment_by_id(db, equipment_id)
    if not db_equipment:
        return None
    
    db_equipment.is_deleted = 1
    db.commit()
    return db_equipment


# ========== 客户管理 CRUD ==========
def get_customer_list(db: Session, skip: int = 0, limit: int = 10, keyword: Optional[str] = None):
    """获取客户列表"""
    query = db.query(models.Customer).filter(models.Customer.is_deleted == 0)
    
    if keyword:
        query = query.filter(models.Customer.customer_name.contains(keyword))
    
    total = query.count()
    items = query.order_by(models.Customer.created_at.desc()).offset(skip).limit(limit).all()
    
    return {"total": total, "items": items}


def create_customer(db: Session, customer: schemas.CustomerCreate):
    """创建客户"""
    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


# ========== 租赁订单 CRUD ==========
def get_order_list(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    status: Optional[str] = None,
    keyword: Optional[str] = None
):
    """获取订单列表"""
    query = db.query(models.LeaseOrder).filter(models.LeaseOrder.is_deleted == 0)
    
    if status:
        query = query.filter(models.LeaseOrder.status == status)
    if keyword:
        query = query.filter(
            or_(
                models.LeaseOrder.order_code.contains(keyword),
                models.LeaseOrder.customer_name.contains(keyword),
                models.LeaseOrder.voyage_no.contains(keyword)
            )
        )
    
    total = query.count()
    items = query.order_by(models.LeaseOrder.created_at.desc()).offset(skip).limit(limit).all()
    
    return {"total": total, "items": items}


def get_order_by_id(db: Session, order_id: int):
    """根据ID获取订单"""
    return db.query(models.LeaseOrder).filter(
        models.LeaseOrder.order_id == order_id,
        models.LeaseOrder.is_deleted == 0
    ).first()


def create_order(db: Session, order: schemas.LeaseOrderCreate):
    """创建租赁订单"""
    # 生成订单编号
    order_code = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # 创建订单
    order_dict = order.dict(exclude={'order_items'})
    db_order = models.LeaseOrder(**order_dict, order_code=order_code)
    db.add(db_order)
    db.flush()  # 获取 order_id
    
    # 创建订单明细并计算总额
    total_amount = 0.0
    for item in order.order_items:
        item_dict = item.dict()
        subtotal = item_dict['daily_rate'] * item_dict['rental_days']
        item_dict['subtotal'] = subtotal
        item_dict['order_id'] = db_order.order_id
        
        db_item = models.OrderItem(**item_dict)
        db.add(db_item)
        
        total_amount += subtotal
        
        # 更新设备状态为已出库
        db.query(models.Equipment).filter(
            models.Equipment.equipment_id == item.equipment_id
        ).update({"status": models.EquipmentStatus.OUT})
    
    db_order.total_amount = total_amount
    db.commit()
    db.refresh(db_order)
    
    return db_order


def update_order(db: Session, order_id: int, order: schemas.LeaseOrderUpdate):
    """更新订单"""
    db_order = get_order_by_id(db, order_id)
    if not db_order:
        return None
    
    update_data = order.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_order, key, value)
    
    db.commit()
    db.refresh(db_order)
    return db_order


# ========== 账单管理 CRUD ==========
def get_billing_list(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    status: Optional[str] = None,
    keyword: Optional[str] = None
):
    """获取账单列表"""
    query = db.query(models.Billing).filter(models.Billing.is_deleted == 0)
    
    if status:
        query = query.filter(models.Billing.status == status)
    if keyword:
        query = query.filter(
            or_(
                models.Billing.bill_code.contains(keyword),
                models.Billing.customer_name.contains(keyword)
            )
        )
    
    total = query.count()
    items = query.order_by(models.Billing.created_at.desc()).offset(skip).limit(limit).all()
    
    return {"total": total, "items": items}


def create_billing(db: Session, billing: schemas.BillingCreate):
    """创建账单"""
    bill_code = f"BILL-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    billing_dict = billing.dict()
    total_amount = billing_dict['rental_fee'] + billing_dict['repair_fee'] + billing_dict['other_fee']
    billing_dict['total_amount'] = total_amount
    billing_dict['bill_code'] = bill_code
    
    db_billing = models.Billing(**billing_dict)
    db.add(db_billing)
    db.commit()
    db.refresh(db_billing)
    return db_billing


def update_billing(db: Session, bill_id: int, billing: schemas.BillingUpdate):
    """更新账单"""
    db_billing = db.query(models.Billing).filter(
        models.Billing.bill_id == bill_id,
        models.Billing.is_deleted == 0
    ).first()
    
    if not db_billing:
        return None
    
    update_data = billing.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_billing, key, value)
    
    # 重新计算总额
    db_billing.total_amount = db_billing.rental_fee + db_billing.repair_fee + db_billing.other_fee
    
    db.commit()
    db.refresh(db_billing)
    return db_billing


# ========== 归还与质检 CRUD ==========
def create_return_record(db: Session, return_record: schemas.ReturnRecordCreate):
    """创建归还记录"""
    return_code = f"RET-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    db_return = models.ReturnRecord(
        **return_record.dict(),
        return_code=return_code
    )
    db.add(db_return)
    db.commit()
    db.refresh(db_return)
    return db_return


def create_inspection_record(db: Session, inspection: schemas.InspectionRecordCreate):
    """创建质检记录"""
    # 判断质检结果
    result = models.InspectionResult.PASS
    if inspection.repair_needed == 1 or inspection.function_test == "故障":
        result = models.InspectionResult.REPAIR_NEEDED
    
    db_inspection = models.InspectionRecord(
        **inspection.dict(),
        result=result
    )
    db.add(db_inspection)
    
    # 更新设备状态
    new_status = models.EquipmentStatus.IN_STOCK
    if inspection.repair_needed == 1:
        new_status = models.EquipmentStatus.MAINTENANCE
    
    db.query(models.Equipment).filter(
        models.Equipment.equipment_id == inspection.equipment_id
    ).update({"status": new_status})
    
    db.commit()
    db.refresh(db_inspection)
    return db_inspection


# ========== 统计数据 CRUD ==========
def get_dashboard_stats(db: Session):
    """获取工作台统计数据"""
    # 设备统计
    total_equipment = db.query(func.count(models.Equipment.equipment_id)).filter(
        models.Equipment.is_deleted == 0
    ).scalar()
    
    in_stock = db.query(func.count(models.Equipment.equipment_id)).filter(
        models.Equipment.is_deleted == 0,
        models.Equipment.status == models.EquipmentStatus.IN_STOCK
    ).scalar()
    
    out_stock = db.query(func.count(models.Equipment.equipment_id)).filter(
        models.Equipment.is_deleted == 0,
        models.Equipment.status == models.EquipmentStatus.OUT
    ).scalar()
    
    maintenance = db.query(func.count(models.Equipment.equipment_id)).filter(
        models.Equipment.is_deleted == 0,
        models.Equipment.status == models.EquipmentStatus.MAINTENANCE
    ).scalar()
    
    # 订单统计
    pending_checkout = db.query(func.count(models.LeaseOrder.order_id)).filter(
        models.LeaseOrder.is_deleted == 0,
        models.LeaseOrder.status == models.OrderStatus.PENDING
    ).scalar()
    
    in_progress_orders = db.query(func.count(models.LeaseOrder.order_id)).filter(
        models.LeaseOrder.is_deleted == 0,
        models.LeaseOrder.status == models.OrderStatus.IN_PROGRESS
    ).scalar()
    
    # 财务统计
    total_revenue = db.query(func.sum(models.Billing.total_amount)).filter(
        models.Billing.is_deleted == 0,
        models.Billing.status == models.BillingStatus.PAID
    ).scalar() or 0.0
    
    pending_amount = db.query(func.sum(models.Billing.total_amount)).filter(
        models.Billing.is_deleted == 0,
        models.Billing.status.in_([models.BillingStatus.PENDING, models.BillingStatus.CONFIRMED])
    ).scalar() or 0.0
    
    overdue_bills = db.query(func.count(models.Billing.bill_id)).filter(
        models.Billing.is_deleted == 0,
        models.Billing.status == models.BillingStatus.OVERDUE
    ).scalar()
    
    # 质检统计
    pending_inspection = db.query(func.count(models.ReturnRecord.return_id)).filter(
        models.ReturnRecord.inspection_status == "待质检"
    ).scalar()
    
    return schemas.DashboardStats(
        total_equipment=total_equipment or 0,
        in_stock=in_stock or 0,
        out_stock=out_stock or 0,
        maintenance=maintenance or 0,
        pending_checkout=pending_checkout or 0,
        in_progress_orders=in_progress_orders or 0,
        pending_inspection=pending_inspection or 0,
        total_revenue=total_revenue,
        pending_amount=pending_amount,
        overdue_bills=overdue_bills or 0
    )


# ========== 用户管理 CRUD ==========
def get_user_by_username(db: Session, username: str):
    """根据用户名获取用户"""
    return db.query(models.User).filter(
        models.User.username == username,
        models.User.is_deleted == 0
    ).first()


def create_user(db: Session, user: schemas.UserCreate):
    """创建用户"""
    hashed_pwd = hash_password(user.password)
    db_user = models.User(
        **user.dict(exclude={'password'}),
        password_hash=hashed_pwd
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


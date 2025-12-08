from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import enum


# 枚举类型定义
class EquipmentStatus(str, enum.Enum):
    IN_STOCK = "在库"
    OUT = "已出库"
    MAINTENANCE = "维修中"
    SCRAPPED = "已报废"


class OrderStatus(str, enum.Enum):
    PENDING = "待提货"
    IN_PROGRESS = "航次执行中"
    COMPLETED = "已完结"
    CANCELLED = "已取消"


class BillingStatus(str, enum.Enum):
    PENDING = "待确认"
    CONFIRMED = "已确认"
    PAID = "已结清"
    OVERDUE = "逾期"


class InspectionResult(str, enum.Enum):
    PASS = "合格"
    REPAIR_NEEDED = "需维修"
    FAILED = "不合格"


# 设备表
class Equipment(Base):
    __tablename__ = "equipment"

    equipment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    equipment_code = Column(String(50), unique=True, nullable=False, index=True)
    equipment_name = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False, index=True)
    status = Column(Enum(EquipmentStatus), default=EquipmentStatus.IN_STOCK, nullable=False, index=True)
    storage_location = Column(String(100))
    purchase_price = Column(Float, default=0.0)
    daily_rental_rate = Column(Float, default=0.0)
    specifications = Column(Text)
    remarks = Column(Text)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    is_deleted = Column(Integer, default=0)

    # 关系
    order_items = relationship("OrderItem", back_populates="equipment")
    inspection_records = relationship("InspectionRecord", back_populates="equipment")


# 客户表
class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_name = Column(String(200), nullable=False, unique=True)
    contact_person = Column(String(100))
    phone = Column(String(50))
    email = Column(String(100))
    address = Column(String(500))
    credit_rating = Column(String(20))
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    is_deleted = Column(Integer, default=0)

    # 关系
    lease_orders = relationship("LeaseOrder", back_populates="customer")


# 租赁订单表
class LeaseOrder(Base):
    __tablename__ = "lease_orders"

    order_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_code = Column(String(50), unique=True, nullable=False, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    customer_name = Column(String(200), nullable=False)
    voyage_no = Column(String(100), index=True)
    start_date = Column(Date, nullable=False)
    expected_return_date = Column(Date)
    actual_return_date = Column(Date)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False, index=True)
    total_amount = Column(Float, default=0.0)
    remarks = Column(Text)
    created_by = Column(String(100))
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    is_deleted = Column(Integer, default=0)

    # 关系
    customer = relationship("Customer", back_populates="lease_orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    billing = relationship("Billing", back_populates="order", uselist=False)


# 订单明细表
class OrderItem(Base):
    __tablename__ = "order_items"

    item_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("lease_orders.order_id"), nullable=False)
    equipment_id = Column(Integer, ForeignKey("equipment.equipment_id"), nullable=False)
    equipment_code = Column(String(50), nullable=False)
    equipment_name = Column(String(200), nullable=False)
    daily_rate = Column(Float, nullable=False)
    rental_days = Column(Integer, default=0)
    subtotal = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    # 关系
    order = relationship("LeaseOrder", back_populates="order_items")
    equipment = relationship("Equipment", back_populates="order_items")


# 账单表
class Billing(Base):
    __tablename__ = "billing"

    bill_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    bill_code = Column(String(50), unique=True, nullable=False, index=True)
    order_id = Column(Integer, ForeignKey("lease_orders.order_id"), nullable=False)
    customer_name = Column(String(200), nullable=False)
    rental_fee = Column(Float, default=0.0)
    repair_fee = Column(Float, default=0.0)
    other_fee = Column(Float, default=0.0)
    total_amount = Column(Float, default=0.0)
    status = Column(Enum(BillingStatus), default=BillingStatus.PENDING, nullable=False, index=True)
    billing_date = Column(Date, default=datetime.now().date)
    payment_date = Column(Date)
    remarks = Column(Text)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    is_deleted = Column(Integer, default=0)

    # 关系
    order = relationship("LeaseOrder", back_populates="billing")


# 归还记录表
class ReturnRecord(Base):
    __tablename__ = "return_records"

    return_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    return_code = Column(String(50), unique=True, nullable=False, index=True)
    order_id = Column(Integer, ForeignKey("lease_orders.order_id"), nullable=False)
    voyage_no = Column(String(100))
    return_date = Column(DateTime, default=datetime.now, nullable=False)
    return_person = Column(String(100))
    equipment_count = Column(Integer, default=0)
    inspection_status = Column(String(50), default="待质检")
    remarks = Column(Text)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    # 关系
    inspection_records = relationship("InspectionRecord", back_populates="return_record")


# 质检记录表
class InspectionRecord(Base):
    __tablename__ = "inspection_records"

    inspection_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    return_id = Column(Integer, ForeignKey("return_records.return_id"), nullable=False)
    equipment_id = Column(Integer, ForeignKey("equipment.equipment_id"), nullable=False)
    equipment_code = Column(String(50), nullable=False)
    inspector = Column(String(100), nullable=False)
    appearance_status = Column(String(50))  # 完好、轻微磨损、严重损坏
    function_test = Column(String(50))  # 通过、故障
    repair_needed = Column(Integer, default=0)  # 0-否, 1-是
    repair_cost = Column(Float, default=0.0)
    result = Column(Enum(InspectionResult), default=InspectionResult.PASS)
    inspection_date = Column(DateTime, default=datetime.now, nullable=False)
    remarks = Column(Text)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    # 关系
    return_record = relationship("ReturnRecord", back_populates="inspection_records")
    equipment = relationship("Equipment", back_populates="inspection_records")


# 用户表
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    real_name = Column(String(100))
    role = Column(String(50), default="operator")  # admin, warehouse, finance, operator
    phone = Column(String(50))
    email = Column(String(100))
    status = Column(String(20), default="active")  # active, inactive
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    is_deleted = Column(Integer, default=0)


# 操作日志表
class OperationLog(Base):
    __tablename__ = "operation_logs"

    log_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer)
    username = Column(String(100))
    action = Column(String(50), nullable=False)  # INSERT, UPDATE, DELETE, QUERY
    table_name = Column(String(100))
    record_id = Column(String(100))
    description = Column(Text)
    ip_address = Column(String(50))
    created_at = Column(DateTime, default=datetime.now, nullable=False, index=True)


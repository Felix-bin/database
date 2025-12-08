from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from models import EquipmentStatus, OrderStatus, BillingStatus, InspectionResult


# 设备相关 Schemas
class EquipmentBase(BaseModel):
    equipment_code: str
    equipment_name: str
    category: str
    storage_location: Optional[str] = None
    purchase_price: Optional[float] = 0.0
    daily_rental_rate: Optional[float] = 0.0
    specifications: Optional[str] = None
    remarks: Optional[str] = None


class EquipmentCreate(EquipmentBase):
    pass


class EquipmentUpdate(BaseModel):
    equipment_name: Optional[str] = None
    category: Optional[str] = None
    status: Optional[EquipmentStatus] = None
    storage_location: Optional[str] = None
    daily_rental_rate: Optional[float] = None
    specifications: Optional[str] = None
    remarks: Optional[str] = None


class Equipment(EquipmentBase):
    equipment_id: int
    status: EquipmentStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# 客户相关 Schemas
class CustomerBase(BaseModel):
    customer_name: str
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    credit_rating: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    customer_name: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    credit_rating: Optional[str] = None


class Customer(CustomerBase):
    customer_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# 订单明细 Schemas
class OrderItemBase(BaseModel):
    equipment_id: int
    equipment_code: str
    equipment_name: str
    daily_rate: float
    rental_days: Optional[int] = 0


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    item_id: int
    order_id: int
    subtotal: float
    created_at: datetime

    class Config:
        from_attributes = True


# 租赁订单 Schemas
class LeaseOrderBase(BaseModel):
    customer_id: int
    customer_name: str
    voyage_no: Optional[str] = None
    start_date: date
    expected_return_date: Optional[date] = None
    remarks: Optional[str] = None


class LeaseOrderCreate(LeaseOrderBase):
    order_items: List[OrderItemCreate]
    created_by: Optional[str] = None


class LeaseOrderUpdate(BaseModel):
    voyage_no: Optional[str] = None
    expected_return_date: Optional[date] = None
    actual_return_date: Optional[date] = None
    status: Optional[OrderStatus] = None
    remarks: Optional[str] = None


class LeaseOrder(LeaseOrderBase):
    order_id: int
    order_code: str
    status: OrderStatus
    total_amount: float
    actual_return_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime
    order_items: List[OrderItem] = []

    class Config:
        from_attributes = True


# 账单 Schemas
class BillingBase(BaseModel):
    order_id: int
    customer_name: str
    rental_fee: float = 0.0
    repair_fee: float = 0.0
    other_fee: float = 0.0


class BillingCreate(BillingBase):
    pass


class BillingUpdate(BaseModel):
    rental_fee: Optional[float] = None
    repair_fee: Optional[float] = None
    other_fee: Optional[float] = None
    status: Optional[BillingStatus] = None
    payment_date: Optional[date] = None
    remarks: Optional[str] = None


class Billing(BillingBase):
    bill_id: int
    bill_code: str
    total_amount: float
    status: BillingStatus
    billing_date: date
    payment_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# 归还记录 Schemas
class ReturnRecordBase(BaseModel):
    order_id: int
    voyage_no: Optional[str] = None
    return_person: Optional[str] = None
    equipment_count: int = 0
    remarks: Optional[str] = None


class ReturnRecordCreate(ReturnRecordBase):
    pass


class ReturnRecord(ReturnRecordBase):
    return_id: int
    return_code: str
    return_date: datetime
    inspection_status: str
    created_at: datetime

    class Config:
        from_attributes = True


# 质检记录 Schemas
class InspectionRecordBase(BaseModel):
    equipment_id: int
    equipment_code: str
    inspector: str
    appearance_status: str
    function_test: str
    repair_needed: int = 0
    repair_cost: float = 0.0
    remarks: Optional[str] = None


class InspectionRecordCreate(InspectionRecordBase):
    return_id: int


class InspectionRecord(InspectionRecordBase):
    inspection_id: int
    return_id: int
    result: InspectionResult
    inspection_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True


# 用户 Schemas
class UserBase(BaseModel):
    username: str
    real_name: Optional[str] = None
    role: str = "operator"
    phone: Optional[str] = None
    email: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    real_name: Optional[str] = None
    role: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    status: Optional[str] = None


class User(UserBase):
    user_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# 通用响应 Schema
class Response(BaseModel):
    code: int = 200
    message: str = "success"
    data: Optional[dict] = None


# 分页响应 Schema
class PageResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: List = []
    total: int = 0
    page: int = 1
    page_size: int = 10


# 统计数据 Schema
class DashboardStats(BaseModel):
    total_equipment: int = 0
    in_stock: int = 0
    out_stock: int = 0
    maintenance: int = 0
    pending_checkout: int = 0
    in_progress_orders: int = 0
    pending_inspection: int = 0
    total_revenue: float = 0.0
    pending_amount: float = 0.0
    overdue_bills: int = 0


from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrderItemBase(BaseModel):
    menu_item_id: int
    quantity: float
    unit_price: float
    notes: Optional[str] = None
    
    class Config:
        orm_mode = True

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemResponse(OrderItemBase):
    id: int
    order_id: int
    status: str

class OrderBase(BaseModel):
    table_id: int
    status: str = "pending"
    notes: Optional[str] = None

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    updated_at: datetime
    total_amount: float
    is_paid: bool
    items: List[OrderItemResponse] = []
    
    class Config:
        orm_mode = True

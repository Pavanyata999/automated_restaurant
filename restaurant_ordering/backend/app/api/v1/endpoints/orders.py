from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...db.session import get_db
from ...models.order import Order, OrderItem
from ...schemas.order import OrderCreate, OrderResponse, OrderItemCreate

router = APIRouter()

@router.get("/", response_model=List[OrderResponse])
async def get_orders(db: Session = Depends(get_db)):
    """Get all orders"""
    orders = db.query(Order).all()
    return orders

@router.post("/", response_model=OrderResponse)
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """Create a new order"""
    db_order = Order(
        table_id=order.table_id,
        status="pending",
        total_amount=0.0
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    total = 0.0
    for item_data in order.items:
        order_item = OrderItem(
            order_id=db_order.id,
            menu_item_id=item_data.menu_item_id,
            quantity=item_data.quantity,
            unit_price=item_data.unit_price
        )
        total += item_data.quantity * item_data.unit_price
        db.add(order_item)
    
    db_order.total_amount = total
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, db: Session = Depends(get_db)):
    """Get a specific order"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/{order_id}/status")
async def update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):
    """Update order status"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = status
    db.commit()
    return {"message": f"Order status updated to {status}"}

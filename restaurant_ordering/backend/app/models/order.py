from sqlalchemy import Column, String, Enum, Float, ForeignKey, DateTime, Boolean, Text, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.session import Base

class Order(Base):
    """Order model for customer orders"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=False)
    server_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(
        Enum('pending', 'confirmed', 'preparing', 'ready', 'served', 'completed', 'cancelled', 
             name='order_status'),
        default='pending',
        nullable=False
    )
    notes = Column(Text, nullable=True)
    is_paid = Column(Boolean, default=False, nullable=False)
    served_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    total_amount = Column(Float, default=0.0)
    
    # Relationships
    table = relationship("Table", back_populates="orders")
    server = relationship("User", back_populates="orders_served")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    bill = relationship("Bill", back_populates="order", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Order {self.id} - {self.status}>"
    
    @property
    def total_amount(self):
        return sum(item.subtotal for item in self.items)
    
    @property
    def is_active(self):
        return self.status not in ['completed', 'cancelled']
    
    def update_status(self, new_status, commit=True, db=None):
        self.status = new_status
        now = datetime.utcnow()
        
        if new_status == 'served':
            self.served_at = now
        elif new_status in ['completed', 'cancelled']:
            self.completed_at = now
        
        if commit and db:
            db.commit()
            db.refresh(self)
        
        return self


class OrderItem(Base):
    """Individual items within an order"""
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    quantity = Column(Float, default=1, nullable=False)  # Float to allow for half portions
    unit_price = Column(Float, nullable=False)  # Price at time of ordering
    notes = Column(Text, nullable=True)
    status = Column(
        Enum('pending', 'preparing', 'ready', 'served', 'cancelled', name='order_item_status'),
        default='pending',
        nullable=False
    )
    
    # Relationships
    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem", back_populates="order_items")
    
    def __repr__(self):
        return f"<OrderItem {self.menu_item.name} x{self.quantity}>"
    
    @property
    def subtotal(self):
        return self.unit_price * self.quantity
    
    @property
    def formatted_subtotal(self):
        return f"${self.subtotal:.2f}"
    
    @property
    def formatted_unit_price(self):
        return f"${self.unit_price:.2f}"

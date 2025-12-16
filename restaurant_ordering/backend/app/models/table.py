from sqlalchemy import Column, String, Enum, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..db.session import Base

class Table(Base):
    """Restaurant table model"""
    __tablename__ = "tables"
    
    id = Column(Integer, primary_key=True, index=True)
    table_number = Column(String(10), unique=True, nullable=False)
    capacity = Column(Integer, default=4)
    status = Column(
        Enum('available', 'occupied', 'reserved', 'cleaning', name='table_status'),
        default='available',
        nullable=False
    )
    qr_code = Column(String(255), unique=True, nullable=True)  # URL to QR code image
    
    # Relationships
    orders = relationship("Order", back_populates="table", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Table {self.table_number}>"
    
    @property
    def is_available(self):
        return self.status == 'available'
    
    @property
    def current_order(self):
        # Get the most recent active order
        active_orders = [o for o in self.orders if o.status not in ['completed', 'cancelled']]
        return active_orders[0] if active_orders else None

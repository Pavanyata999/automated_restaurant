from sqlalchemy import Column, Float, ForeignKey, Enum, Integer, Text
from sqlalchemy.orm import relationship
from .base import BaseModel

class Bill(BaseModel):
    """Bill model for order payments"""
    __tablename__ = "bills"
    
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True, nullable=False)
    subtotal = Column(Float, nullable=False)
    tax_amount = Column(Float, nullable=False)  # GST amount
    service_charge = Column(Float, default=0.0, nullable=False)
    discount_amount = Column(Float, default=0.0, nullable=False)
    total_amount = Column(Float, nullable=False)
    payment_status = Column(
        Enum('pending', 'partially_paid', 'paid', 'refunded', 'failed', name='payment_status'),
        default='pending',
        nullable=False
    )
    payment_method = Column(
        Enum('cash', 'card', 'upi', 'wallet', 'split', name='payment_methods'),
        nullable=True
    )
    payment_details = Column(Text, nullable=True)  # Store payment gateway response
    
    # Relationships
    order = relationship("Order", back_populates="bill")
    
    def __repr__(self):
        return f"<Bill {self.id} - {self.payment_status}>"
    
    @property
    def formatted_subtotal(self):
        return f"${self.subtotal:.2f}"
    
    @property
    def formatted_tax(self):
        return f"${self.tax_amount:.2f}"
    
    @property
    def formatted_service_charge(self):
        return f"${self.service_charge:.2f}"
    
    @property
    def formatted_discount(self):
        return f"${self.discount_amount:.2f}"
    
    @property
    def formatted_total(self):
        return f"${self.total_amount:.2f}"

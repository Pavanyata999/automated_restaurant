from sqlalchemy import Column, String, Float, Boolean, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .base import BaseModel

class MenuItem(BaseModel):
    """Menu item model for the restaurant"""
    __tablename__ = "menu_items"
    
    name = Column(String(100), nullable=False, index=True)
    description = Column(String(500), nullable=True)
    price = Column(Float, nullable=False)
    category = Column(
        Enum('starter', 'main', 'dessert', 'beverage', 'alcohol', name='menu_categories'),
        nullable=False
    )
    image_url = Column(String(500), nullable=True)
    is_available = Column(Boolean, default=True, nullable=False)
    preparation_time = Column(Integer, default=15)  # in minutes
    
    # Relationships
    order_items = relationship("OrderItem", back_populates="menu_item")
    
    def __repr__(self):
        return f"<MenuItem {self.name}>"
    
    @property
    def formatted_price(self):
        return f"${self.price:.2f}"

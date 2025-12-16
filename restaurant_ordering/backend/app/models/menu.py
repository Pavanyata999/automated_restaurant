from sqlalchemy import Column, Integer, String, Float, Boolean, Text
from ..db.session import Base

class MenuItem(Base):
    __tablename__ = "menu_items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    is_available = Column(Boolean, default=True)
    image_url = Column(String(255))
    
    def __repr__(self):
        return f"<MenuItem(name={self.name}, price={self.price})>"

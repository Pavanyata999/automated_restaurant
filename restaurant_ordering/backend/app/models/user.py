from sqlalchemy import Column, String, Boolean, Enum, Integer
from sqlalchemy.orm import relationship
from ..db.session import Base

class User(Base):
    """User model for authentication and authorization"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    role = Column(Enum('admin', 'chef', 'server', name='user_roles'), nullable=False, default='server')
    
    # Relationships
    orders_served = relationship("Order", back_populates="server", foreign_keys="Order.server_id")
    
    def __repr__(self):
        return f"<User {self.email}>"
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    @property
    def is_chef(self):
        return self.role == 'chef'
    
    @property
    def is_server(self):
        return self.role == 'server' or self.is_admin

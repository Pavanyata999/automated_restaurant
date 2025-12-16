from datetime import datetime
from typing import Any, Optional
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class BaseModel:
    __name__: str
    __allow_unmapped__ = True  # Allow unmapped attributes
    
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    
    # Common columns for all tables
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            c.name: getattr(self, c.name) 
            for c in self.__table__.columns
        }

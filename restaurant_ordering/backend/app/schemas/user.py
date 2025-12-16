from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum
from datetime import datetime

class UserRole(str, Enum):
    """User roles"""
    admin = "admin"
    chef = "chef"
    server = "server"
    customer = "customer"

class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRole = UserRole.server

class UserCreate(UserBase):
    """Schema for creating a user"""
    password: str = Field(..., min_length=6)

class UserUpdate(BaseModel):
    """Schema for updating a user"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=6)
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None

class UserInDBBase(UserBase):
    """Base user in database schema"""
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class User(UserInDBBase):
    """User schema for API responses"""
    pass

class UserResponse(User):
    """Alias for User schema for consistency"""
    pass

class UserInDB(UserInDBBase):
    """User schema for internal use"""
    hashed_password: str

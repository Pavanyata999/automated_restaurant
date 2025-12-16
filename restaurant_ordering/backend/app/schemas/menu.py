from pydantic import BaseModel
from typing import Optional

class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str
    is_available: bool = True
    image_url: Optional[str] = None

    class Config:
        orm_mode = True

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemUpdate(MenuItemBase):
    pass

class MenuItemResponse(MenuItemBase):
    id: int

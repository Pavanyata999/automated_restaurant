from pydantic import BaseModel
from typing import Optional

class TableBase(BaseModel):
    table_number: str
    capacity: int = 4
    status: str = "available"
    qr_code: Optional[str] = None
    
    class Config:
        orm_mode = True

class TableCreate(TableBase):
    pass

class TableUpdate(TableBase):
    pass

class TableResponse(TableBase):
    id: int

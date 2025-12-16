from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...db.session import get_db
from ...models.table import Table
from ...schemas.table import TableCreate, TableResponse

router = APIRouter()

@router.get("/", response_model=List[TableResponse])
async def get_tables(db: Session = Depends(get_db)):
    """Get all tables"""
    tables = db.query(Table).all()
    return tables

@router.post("/", response_model=TableResponse)
async def create_table(table: TableCreate, db: Session = Depends(get_db)):
    """Create a new table"""
    db_table = Table(**table.dict())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table

@router.get("/{table_id}", response_model=TableResponse)
async def get_table(table_id: int, db: Session = Depends(get_db)):
    """Get a specific table"""
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    return table

@router.put("/{table_id}", response_model=TableResponse)
async def update_table(table_id: int, table_update: TableCreate, db: Session = Depends(get_db)):
    """Update a table"""
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    
    for key, value in table_update.dict().items():
        setattr(table, key, value)
    
    db.commit()
    db.refresh(table)
    return table

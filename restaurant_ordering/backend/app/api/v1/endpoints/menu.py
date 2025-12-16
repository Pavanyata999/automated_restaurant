from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...db.session import get_db
from ...models.menu import MenuItem
from ...schemas.menu import MenuItemCreate, MenuItemResponse

router = APIRouter()

@router.get("/", response_model=List[MenuItemResponse])
async def get_menu_items(db: Session = Depends(get_db)):
    """Get all menu items"""
    items = db.query(MenuItem).all()
    return items

@router.post("/", response_model=MenuItemResponse)
async def create_menu_item(item: MenuItemCreate, db: Session = Depends(get_db)):
    """Create a new menu item"""
    db_item = MenuItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/{item_id}", response_model=MenuItemResponse)
async def get_menu_item(item_id: int, db: Session = Depends(get_db)):
    """Get a specific menu item"""
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item

@router.put("/{item_id}", response_model=MenuItemResponse)
async def update_menu_item(item_id: int, item_update: MenuItemCreate, db: Session = Depends(get_db)):
    """Update a menu item"""
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    for key, value in item_update.dict().items():
        setattr(item, key, value)
    
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}")
async def delete_menu_item(item_id: int, db: Session = Depends(get_db)):
    """Delete a menu item"""
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    db.delete(item)
    db.commit()
    return {"message": "Menu item deleted successfully"}

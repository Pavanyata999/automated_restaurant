from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Restaurant Ordering System API")

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample data
menu_items = [
    {"id": 1, "name": "Burger", "price": 12.99, "category": "Main", "available": True},
    {"id": 2, "name": "Pizza", "price": 15.99, "category": "Main", "available": True},
    {"id": 3, "name": "Salad", "price": 8.99, "category": "Starter", "available": True},
    {"id": 4, "name": "Soda", "price": 2.99, "category": "Drink", "available": True},
]

tables = [
    {"id": 1, "number": "T1", "capacity": 4, "status": "available"},
    {"id": 2, "number": "T2", "capacity": 4, "status": "available"},
    {"id": 3, "number": "T3", "capacity": 6, "status": "available"},
]

orders = []

@app.get("/")
async def root():
    return {"message": "Restaurant Ordering System API"}

@app.get("/api/v1/menu")
async def get_menu():
    return menu_items

@app.get("/api/v1/menu/{item_id}")
async def get_menu_item(item_id: int):
    item = next((item for item in menu_items if item["id"] == item_id), None)
    if not item:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item

@app.get("/api/v1/tables")
async def get_tables():
    return tables

@app.get("/api/v1/orders")
async def get_orders():
    return orders

@app.post("/api/v1/orders")
async def create_order(order_data: dict):
    order = {
        "id": len(orders) + 1,
        "table_id": order_data.get("table_id"),
        "items": order_data.get("items", []),
        "status": "pending",
        "total": sum(item["price"] * item.get("quantity", 1) for item in order_data.get("items", []))
    }
    orders.append(order)
    return order

@app.get("/api/v1/orders/{order_id}")
async def get_order(order_id: int):
    order = next((order for order in orders if order["id"] == order_id), None)
    if not order:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.put("/api/v1/orders/{order_id}/status")
async def update_order_status(order_id: int, status_data: dict):
    order = next((order for order in orders if order["id"] == order_id), None)
    if not order:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Order not found")
    order["status"] = status_data.get("status", "pending")
    return order

if __name__ == "__main__":
    uvicorn.run("simple_main:app", host="0.0.0.0", port=8001, reload=True)

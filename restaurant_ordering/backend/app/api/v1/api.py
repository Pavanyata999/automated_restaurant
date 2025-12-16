from fastapi import APIRouter
from .endpoints import auth, users, tables, menu, orders

api_router = APIRouter()

# Include all API endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(tables.router, prefix="/tables", tags=["Tables"])
api_router.include_router(menu.router, prefix="/menu", tags=["Menu"])
api_router.include_router(orders.router, prefix="/orders", tags=["Orders"])

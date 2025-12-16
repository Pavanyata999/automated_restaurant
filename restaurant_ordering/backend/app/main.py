from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from fastapi.middleware.gzip import GZipMiddleware
import uvicorn
import os
from .core.config import settings
from .api.v1.api import api_router
from .db.session import engine, Base
from .core.security import get_current_active_user
from .models import User

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create default admin user if not exists
    async with engine.begin() as conn:
        from sqlalchemy import select
        from .core.security import get_password_hash
        
        admin = await conn.execute(select(User).where(User.email == settings.FIRST_SUPERUSER))
        if not admin.scalar_one_or_none():
            hashed_password = get_password_hash(settings.FIRST_SUPERUSER_PASSWORD)
            admin = User(
                email=settings.FIRST_SUPERUSER,
                hashed_password=hashed_password,
                is_superuser=True,
                full_name="Admin",
                role="admin"
            )
            conn.add(admin)
            await conn.commit()
    
    yield
    
    # Clean up on shutdown
    await engine.dispose()

app = FastAPI(
    title="Restaurant Ordering System API",
    description="Backend API for the Digital Restaurant Ordering System",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add GZip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include API router
app.include_router(api_router, prefix="/api/v1")

# Serve static files for the frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message": "Welcome to the Restaurant Ordering System API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

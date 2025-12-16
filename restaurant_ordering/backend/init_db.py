import sys
from sqlalchemy.orm import Session
from app.db.session import engine, Base, SessionLocal
from app.models import *  # noqa
from app.core.security import get_password_hash

def init_db():
    # Create all tables first
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
    
    db = SessionLocal()
    
    try:
        # Create default admin user if not exists
        admin = db.query(User).filter(User.email == "admin@restaurant.com").first()
        if not admin:
            admin_user = User(
                email="admin@restaurant.com",
                hashed_password=get_password_hash("admin123"),
                full_name="Admin User",
                is_superuser=True,
                is_active=True,
                role="admin"
            )
            db.add(admin_user)
            db.commit()
            print("✅ Created admin user")
        
        # Create some sample tables
        if db.query(Table).count() == 0:
            for i in range(1, 6):
                table = Table(
                    table_number=f"T{i:02d}",
                    capacity=4 if i < 4 else 6,
                    status="available"
                )
                db.add(table)
            db.commit()
            print("✅ Created sample tables")
        
        # Create some sample menu items
        if db.query(MenuItem).count() == 0:
            menu_items = [
                {"name": "Garlic Bread", "category": "starter", "price": 5.99, "preparation_time": 10},
                {"name": "Bruschetta", "category": "starter", "price": 7.50, "preparation_time": 15},
                {"name": "Margherita Pizza", "category": "main", "price": 12.99, "preparation_time": 20},
                {"name": "Pasta Carbonara", "category": "main", "price": 14.99, "preparation_time": 25},
                {"name": "Caesar Salad", "category": "main", "price": 10.50, "preparation_time": 15},
                {"name": "Chocolate Lava Cake", "category": "dessert", "price": 6.99, "preparation_time": 10},
                {"name": "Coke", "category": "beverage", "price": 2.50, "preparation_time": 2},
                {"name": "Iced Tea", "category": "beverage", "price": 2.99, "preparation_time": 2},
            ]
            
            for item in menu_items:
                menu_item = MenuItem(
                    name=item["name"],
                    category=item["category"],
                    price=item["price"],
                    preparation_time=item["preparation_time"],
                    is_available=True
                )
                db.add(menu_item)
            
            db.commit()
            print("✅ Created sample menu items")
            
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("✅ Database initialization complete")

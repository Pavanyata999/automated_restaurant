# Import all models here so they're available when the application starts
from ..db.session import Base
from .user import User
from .table import Table
from .menu import MenuItem
from .order import Order, OrderItem
from .bill import Bill

# This ensures SQLAlchemy knows about all models
__all__ = ['Base', 'User', 'Table', 'MenuItem', 'Order', 'OrderItem', 'Bill']

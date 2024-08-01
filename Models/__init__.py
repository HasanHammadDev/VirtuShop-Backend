from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .order import Order, OrderItem
from .product import Product
from .reviews import Review
from .user import User
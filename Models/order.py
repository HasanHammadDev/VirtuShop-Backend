from . import db

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    total_price = db.Column(db.Numeric(10, 2))
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    
    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Numeric(10, 2))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

# db = SQLAlchemy()

# class User(db.Model):
#     __tablename__ = 'users'
#     User_id = db.column(db.Integer, primary_key=True)
#     full_name = db.column(db.String(255), nullable=False)
#     email = db.column(db.String(255), unique=True, nullable=False)
#     phone_number = db.column(db.string(50))
#     registered_at = db.Column(db.DateTime, default=datetime.utcnow)
#     password_hash = db.Column(db.Text, nullable=False)
#     role = db.Column(db.String(50), default='customer')
    
#     orders = db.relationship('Order', backref='customer', lazy=True, foreign_keys='Order.customer_id')
#     managed_orders = db.relationship('Order', backref='staff_member', lazy=True, foreign_keys='Order.staff_id')
#     reservations = db.relationship('Reservation', backref='customer', lazy=True, foreign_keys='Reservation.customer_id')


# class MenuItem(db.Model):
#     __tablename__ = 'menu_items'
#     item_id = db.Column(db.Integer, primary_key=True)
#     item_name = db.Column(db.String(255), nullable=False)
#     description = db.Column(db.Text)
#     price = db.Column(db.Numeric(10, 2), nullable=False)
#     category = db.Column(db.String(100))
#     available = db.Column(db.Boolean, default=True)

#     order_items = db.relationship('OrderItem', backref='menu_item', lazy=True)


# class Order(db.Model):
#     __tablename__ = 'orders'
#     order_id = db.Column(db.Integer, primary_key=True)
#     customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
#     order_date = db.Column(db.DateTime, default=datetime.utcnow)
#     status = db.column(db.String(50), default='pending')
#     total_amount = db.column(db.Numeric(10, 2), nullable=False)

#     order_items = db.relationship('OrderItem', backref='order', lazy=True)
#     payment = db.relationship('Payment', backref='order', uselist=False)


# class OrderItem(db.Model):
#     __tablename__ = 'order_items'
#     order_item_id = db.Column(db.Integer, primary_key=True)
#     order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
#     item_id = db.Column(db.Integer, db.ForeignKey('menu_items.item_id'), nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)
#     subtotal = db.Column(db.Numeric(10, 2), nullable=False)


# class Table(db.Model):
#     __tablename__ = 'tables'
#     table_id = db.Column(db.Integer, primary_key=True)
#     table_number = db.Column(db.Integer, unique=True, nullable=False)
#     capacity = db.Column(db.Integer, nullable=False)
#     status = db.Column(db.String(50), default='available')

#     reservations = db.relationship('Reservation', backref='table', lazy=True)


# class Reservation(db.Model):
#     __tablename__ = 'reservations'
#     reservation_id = db.Column(db.Integer, primary_key=True)
#     customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
#     table_id = db.Column(db.Integer, db.ForignKey('tables.table_id'), nullable=False)
#     reservation_time = db.Column(db.DateTime, nullable=False)
#     guest_count = db.Column(db.Integer, nullable=False)
#     status = db.Column(db.String(50), default='booked')


# class Payment(db.Model):
#     __tablename__ = 'payments'
#     payment_id = db.Column(db.Integer, primary_key=True)
#     order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
#     payment_method = db.Column(db.String(50), nullable=False)
#     amount_paid = db.Column(db.Numeric(10, 2), nullable=False)
#     payment_time = db.Column(db.DateTime, default=datetime.utcnow)


# class Announcement(db.Model):
#     __tablename__ = 'announcements'
#     announcement_id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(255), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     posted_at = db.Column(db.DateTime, default=datetime.utcnow)

#     admin_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
#     admin = db.relationship('User', backref='announcements', foreign_keys=[admin_id])

# class Review(db.Model):
#     __tablename__ = 'reviews'
#     review_id = db.Column(db.Integer, primary_key=True)
#     customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
#     item_id = db.Column(db.Integer, db.ForeignKey('menu_items.item_id'), nullable=False)
#     rating = db.Column(db.Integer)
#     comment = db.Column(db.Text)
#     review_date = db.Column(db.DateTime)
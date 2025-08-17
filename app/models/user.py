from ..extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False,index=True)
    phone_number = db.Column(db.String(50),nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    receive_offers = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def set_password(self,password):
        self.password_hash=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    # orders = db.relationship('Order', backref='customer', lazy=True, foreign_keys='Order.customer_id')
    # managed_orders = db.relationship('Order', backref='staff_member', lazy=True, foreign_keys='Order.staff_id')
    # reservations = db.relationship('Reservation', backref='customer', lazy=True, foreign_keys='Reservation.customer_id')

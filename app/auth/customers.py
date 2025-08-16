# from flask import Blueprint, request, jsonify
# from models import db, Customer
# from datetime import datetime

# bp_customers = Blueprint('customers', __name__, url_prefix='/customers')

# @bp_customers.route('/', methods=['GET'])
# def get_customers():
#     customers = Customer.query.all()
#     return jsonify([{
#         "id" : c.customer_id,
#         "name" : c.full_name,
#         "email" : c.email,
#         "phone" : c.phone_number
#     } for c in customers])

# bp_customers.route('/', methods=['POST'])
# def add_customer():
#     data = request.get_json
#     customer = Customer(
#         full_name =data['full_name'],
#         email=data['email'],
#         phone_number=data.get['phone_number'],
#         password_hash=data['password_hash'],
#         registered_at=datetime.now()
#     )
#     db.session.add(customer)
#     db.session.commit()
#     return jsonify({"message" : "Customer created"}), 201    
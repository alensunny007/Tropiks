# from flask import Flask, jsonify
# from config import Config
# from models import db
# from app.auth.customers import bp_customers


# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)


#     db.init_app(app)
    
#     with app.app_context():
#         db.create_all()


#     @app.route('/')
#     def home():
#         return jsonify({"message": "Tropiks Restaurant backend is running"})



#     app.register_blueprint(bp_customers)


#     return app


# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True)
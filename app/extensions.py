from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db=SQLAlchemy()
login_manager=LoginManager()
mail=Mail()
login_manager.login_view='auth.login'

@login_manager.user_loader
def load_user(user_id):
    from .models.user import User
    return User.query.get(int(user_id))
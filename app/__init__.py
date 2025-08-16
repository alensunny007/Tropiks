from flask import Flask
from .config import config
from .extensions import db,login_manager
from.auth import auth_bp
from .main import main_bp
from flask_migrate import Migrate

migrate=Migrate()
def create_app(config_name='default'):
    app=Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app,db)

    app.register_blueprint(auth_bp,url_prefix='/auth')
    app.register_blueprint(main_bp)

    return app


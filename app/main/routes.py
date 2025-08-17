from flask import render_template,redirect,request,url_for,flash,jsonify
from flask_login import login_required,current_user
from ..extensions import db
from . import main_bp
from sqlalchemy.sql import func

@main_bp.route('/')
def home():
    return render_template('main/home.html')

@main_bp.route('/menu')
def menu():
    return render_template('main/menu.html')
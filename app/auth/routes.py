# auth/routes.py
from flask import render_template, redirect, url_for, flash, current_app, request
from flask_login import login_user, logout_user, login_required, current_user
from ..models.user import User
from .forms import SignUpForm, LoginForm  # Import from local forms module
from . import auth_bp  # Blueprint import
from ..extensions import db

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))  # Use blueprint.route format
    
    form = SignUpForm()
    
    if form.validate_on_submit():
        # Clean phone number
        clean_phone = ''.join(filter(str.isdigit, form.phone_number.data))
        
        # Create new user
        user = User(
            full_name=form.full_name.data.strip(),
            email=form.email.data.lower().strip(),
            phone_number=clean_phone,
            receive_offers=form.receive_offers.data
        )
        user.set_password(form.password.data)
        
        try:
            db.session.add(user)
            db.session.commit()
            
            # Log the user in
            login_user(user)
            
            flash('Account created successfully! Welcome to Tropiks!', 'success')
            return redirect(url_for('main.menu'))  # Use blueprint.route format
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating your account. Please try again.', 'error')
            current_app.logger.error(f'Signup error: {str(e)}')  # Use current_app instead of app
    
    return render_template('auth/signup.html', form=form)

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower().strip()).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            
            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            if next_page:
                # Validate next_page to prevent redirect attacks
                from urllib.parse import urlparse
                if urlparse(next_page).netloc == '':
                    flash(f'Welcome back, {user.full_name}!', 'success')
                    return redirect(next_page)
            
            flash(f'Welcome back, {user.full_name}!', 'success')
            return redirect(url_for('main.menu'))
        else:
            flash('Invalid email or password. Please try again.', 'error')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))  # Redirect to auth blueprint login
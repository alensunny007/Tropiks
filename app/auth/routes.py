# auth/routes.py
from flask import render_template, redirect, url_for, flash, current_app, request
from flask_login import login_user, logout_user, login_required, current_user
from ..models.user import User
from .forms import SignUpForm, LoginForm,ForgotPasswordForm,ResetPasswordForm # Import from local forms module
from . import auth_bp  # Blueprint import
from ..extensions import db
from ..utils import generate_reset_token,verify_reset_token,send_reset_email

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

@auth_bp.route('/forgot-password',methods=['GET','POST'])
def forgot_password():
    form=ForgotPasswordForm()
    if form.validate_on_submit():
        email=form.email.data
        user=User.query.filter_by(email=email).first()
        if user:
            token=generate_reset_token(email)
            reset_url=url_for('auth.reset_password',token=token,_external=True)
            try:
                send_reset_email(email,reset_url)
                flash('Password reset email sent.Check your inbox.',category='success')
            except Exception as e:
                current_app.logger.error(f"Email send err:{e}")
                flash('Error sending email.Please try again.',category='danger')
        else:
            flash('If that email exists a reset link has been sent.',category='info')
        return redirect(url_for('auth.login'))
    return render_template('auth/forgot_pass.html',form=form)

@auth_bp.route('/reset-password/<token>',methods=['GET','POST'])
def reset_password(token):
    email=verify_reset_token(token)
    if not email:
        flash("Invalid or expired reset link",category='danger')
        return redirect(url_for('auth.forgot_password'))
    form=ResetPasswordForm()
    if form.validate_on_submit():
        # print(f"=== PASSWORD RESET DEBUG ===")
        # print(f"Email from token: {email}")
        
        user=User.query.filter_by(email=email).first()
        if user:
            # print(f"User found: {user.username}")
            # print(f"Original hash: {user.password_hash[:20]}...")
            
            # Test the new password
            new_password = form.password.data
            # print(f"New password: {new_password}")
            
            user.set_password(new_password)
            # print(f"Hash after set_password: {user.password_hash[:20]}...")
            
            # Check if SQLAlchemy detected the change
            # print(f"SQLAlchemy dirty objects: {db.session.dirty}")
            # print(f"User in dirty objects: {user in db.session.dirty}")
            
            db.session.commit()
            # print("Commit executed")
            
            # Fresh query to verify
            fresh_user = User.query.filter_by(email=email).first()
            # print(f"Fresh query hash: {fresh_user.password_hash[:20]}...")
            
            # Test if new password works
            test_result = fresh_user.check_password(new_password)
            # print(f"New password check result: {test_result}")
            
            # print(f"=== END DEBUG ===")
            
            flash("Your password has been reset",category='success')
            return redirect(url_for('auth.login'))
        else:
            flash('User not found',category='danger')
            return redirect(url_for('auth.forgot_password'))
    else:
        print(f"Form errors: {form.errors}")
    
    return render_template('auth/reset_pass.html',form=form,token=token)
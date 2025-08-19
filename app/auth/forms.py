from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Email,Length,EqualTo,Regexp
from wtforms.widgets import TextInput,PasswordInput

class SignUpForm(FlaskForm):
    full_name = StringField(
        'Full Name', 
        validators=[
            DataRequired(message="Full name is required"),
            Length(min=2, max=100, message="Full name must be between 2 and 100 characters")
        ],
        render_kw={"placeholder": "John Doe"}
    )
    
    email = StringField(
        'Email', 
        validators=[
            DataRequired(message="Email is required"),
            Email(message="Please enter a valid email address"),
            Length(max=120, message="Email must be less than 120 characters")
        ],
        render_kw={"placeholder": "your@email.com"}
    )
    
    phone_number = StringField(
        'Phone Number',
        validators=[
            DataRequired(message="Phone number is required"),
            Regexp(
                r'^\+?1?-?\.?\s?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})$',
                message="Please enter a valid phone number (e.g., (123) 456-7890)"
            )
        ],
        render_kw={"placeholder": "(123) 456-7890"}
    )
    
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Password is required"),
            Length(min=8, message="Password must be at least 8 characters long"),
            Regexp(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]',
                message="Password must contain at least 1 lowercase letter, 1 uppercase letter, 1 number, and 1 special character"
            )
        ],
        render_kw={"placeholder": "••••••••"}
    )
    
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(message="Please confirm your password"),
            EqualTo('password', message="Passwords must match")
        ],
        render_kw={"placeholder": "••••••••"}
    )
    
    receive_offers = BooleanField(
        'Receive email offers & promotions',
        default=False
    )
    
    submit = SubmitField('Create Account')

class LoginForm(FlaskForm):
    email = StringField(
        'Email', 
        validators=[
            DataRequired(message="Email is required"),
            Email(message="Please enter a valid email address")
        ],
        render_kw={"placeholder": "your@email.com"}
    )
    
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Password is required")
        ],
        render_kw={"placeholder": "••••••••"}
    )
    
    remember_me = BooleanField('Remember Me', default=False)
    submit = SubmitField('Login')

class ForgotPasswordForm(FlaskForm):
    email=StringField("Email",validators=[DataRequired(),Email()])
    submit=SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password=PasswordField('New Password',validators=[DataRequired(),Length(min=8)])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')]) 
    submit=SubmitField('Reset Password')
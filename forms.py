from flask_wtf import FlaskForm
from flask_user import UserManager
from flask_user.forms import RegisterForm
from wtforms import StringField, validators, PasswordField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Email, Length
import email_validator


class CustomRegisterForm(RegisterForm):
    name = StringField(label='Name', validators=[DataRequired()])
    company_name = StringField(label='Company\'s Name')


class CustomUserManager(UserManager):
    def customize(self, app):
        # Configure customized forms
        self.RegisterFormClass = CustomRegisterForm

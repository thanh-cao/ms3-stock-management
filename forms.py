from flask_wtf import FlaskForm
from flask_user import UserManager
from flask_user.forms import RegisterForm
from wtforms import *
from wtforms.validators import *
import email_validator


class CustomRegisterForm(RegisterForm):
    name = StringField(label='Name', validators=[DataRequired()], render_kw={'placeholder': 'Name'})
    company_name = StringField(label='Company\'s Name', render_kw={'placeholder': 'Company\'s Name'})


class CustomUserManager(UserManager):
    def customize(self, app):
        # Configure customized forms
        self.RegisterFormClass = CustomRegisterForm


class UserAccess(FlaskForm):
    username = StringField(Length(min=5, max=10, message='Username name must be between 5 and 10 characters!'),
                            validators=[DataRequired()],
                            render_kw={'placeholder': 'Username'}
                            )
    pin = IntegerField(validators=[Length(max=4), DataRequired()],
                        render_kw={'placeholder': 'Pin code'})
    role = SelectField(choices=[('', 'Choose Role'),
                                ('admin', 'admin'),
                                ('staff', 'staff')],
                        validators=[AnyOf('admin', 'staff')])

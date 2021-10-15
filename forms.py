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
    username = StringField(validators=[Length(min=5, max=10), DataRequired()],
                            render_kw={'placeholder': 'Username'},
                            description='Username name must be between 5 and 10 characters'
                            )        
    pin = IntegerField(validators=[Length(min=4, max=6), DataRequired()],
                        render_kw={'placeholder': 'Pin code'},
                        description='Choose 4 to 6 digits for pin code')
    role = SelectField(choices=[('', 'Choose Role'),
                                ('admin', 'admin'),
                                ('staff', 'staff')],
                        validators=[AnyOf('admin', 'staff')])

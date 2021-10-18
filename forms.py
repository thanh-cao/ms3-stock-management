from flask_wtf import FlaskForm
from flask_user import UserManager
from flask_user.forms import RegisterForm
from wtforms import *
from wtforms.validators import *
from wtforms.fields.html5 import EmailField


class CustomRegisterForm(RegisterForm):
    name = StringField(label='Name',
                       validators=[DataRequired()],
                       render_kw={'placeholder': 'Name'})
    company_name = StringField(label='Company\'s Name',
                               render_kw={'placeholder': 'Company\'s Name'})


class CustomUserManager(UserManager):
    def customize(self, app):
        # Configure customized forms
        self.RegisterFormClass = CustomRegisterForm


class UserAccess(FlaskForm):
    username = StringField(validators=[Length(min=5, max=10), DataRequired()],
                           render_kw={'placeholder': 'Username'},
                           description='Username between 5 and 10 characters')
    pin = IntegerField(validators=[Length(min=4, max=6), DataRequired()],
                       render_kw={'placeholder': 'Pin code'},
                       description='Choose 4 to 6 digits for pin code')
    role = SelectField(choices=[('', 'Choose Role'),
                                ('admin', 'admin'),
                                ('staff', 'staff')],
                       validators=[AnyOf('admin', 'staff')])


class CategoryForm(FlaskForm):
    category_name = StringField(DataRequired(), render_kw={
                                'placeholder': 'Category name'})
    submit = SubmitField(label='Submit')


class SupplierForm(FlaskForm):
    supplier_name = StringField(DataRequired(), render_kw={
                                'placeholder': 'Supplier\'s name'})
    contact_person = StringField(render_kw={'placeholder': 'Contact person'})
    address = StringField(render_kw={'placeholder': 'Address'})
    phone = IntegerField(render_kw={'placeholder': 'Phone'})
    email = EmailField(render_kw={'placeholder': 'Email'})
    submit = SubmitField(label='Submit')

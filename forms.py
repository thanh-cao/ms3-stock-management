from models import Business
from flask_wtf import FlaskForm
from flask_user import UserManager
from flask_user.forms import RegisterForm
from wtforms import *
from wtforms.validators import *
from wtforms.fields.html5 import EmailField, DateField
import datetime


def unique_business_validator(form, field):
    '''
    Form validation that the business name is unique.
    '''
    existing_business = Business.objects(business_name=field.data).first()

    if existing_business:
        raise ValidationError('Business name already exists.')


class CustomRegisterForm(RegisterForm):
    name = StringField(label='Name',
                       validators=[DataRequired()])
    business_name = StringField(label='Business Name',
                                validators=[DataRequired(),
                                            unique_business_validator])


class CustomUserManager(UserManager):
    def customize(self, app):
        # Configure customized forms
        self.RegisterFormClass = CustomRegisterForm


class UserAccess(FlaskForm):
    name = StringField(validators=[Length(min=5, max=10), DataRequired()],
                       render_kw={'placeholder': 'Name'})
    email = EmailField(validators=[Email(), DataRequired()],
                          render_kw={'placeholder': 'Email'})
    password = PasswordField(validators=[DataRequired()],
                                render_kw={'placeholder': 'Password'})
    roles = SelectField(choices=[('', 'Choose Role'),
                                ('admin', 'admin'),
                                ('staff', 'staff')],
                       validators=[AnyOf('admin', 'staff')])


class CategoryForm(FlaskForm):
    category_name = StringField(DataRequired(), render_kw={
                                'placeholder': 'Category name'})
    submit = SubmitField(label='Submit')


class SupplierForm(FlaskForm):
    supplier_name = StringField(validators=[DataRequired()], render_kw={
                                'placeholder': 'Supplier\'s name'})
    contact_person = StringField(render_kw={'placeholder': 'Contact person'})
    address = StringField(render_kw={'placeholder': 'Address'})
    phone = IntegerField(validators=[DataRequired(
                         message='Please input correct digits for phone')],
                         render_kw={'placeholder': 'Phone'})
    email = EmailField(render_kw={'placeholder': 'Email'})
    submit = SubmitField(label='Submit')


class ProductForm(FlaskForm):
    name = StringField(validators=[DataRequired()],
                       render_kw={'placeholder': 'Product name'})
    category_id = SelectField(label='Choose category')
    brand = StringField(render_kw={'placeholder': 'Brand name'})
    supplier_id = SelectField(label='Choose supplier')
    unit_of_measurement = StringField(
        render_kw={'placeholder': 'Unit of measurement'})
    min_stock_allowed = IntegerField(
        render_kw={'placeholder': 'Minimum stock allowed'})
    current_stock = IntegerField(render_kw={'placeholder': 'Current stock'})
    stock_change = IntegerField(render_kw={'placeholder': 'Stock change'})
    submit = SubmitField(label='Submit')


class PendingStockForm(FlaskForm):
    supplier_id = SelectField(label='Choose supplier',
                              validators=[DataRequired()])
    delivery_date = DateField(label='Expected delivery date',
                              validators=[DataRequired()],
                              render_kw={'min': datetime.date.today()})
    submit = SubmitField(label='Submit')


class AddProduct(FlaskForm):
    id = HiddenField()
    name = StringField(validators=[DataRequired()],
                       render_kw={'placeholder': 'Search product',
                                  'class': 'form-control search',
                                  'autocomplete': 'off'})
    expected_stock = IntegerField(validators=[InputRequired(),
                                  NumberRange(min=1, max=100,
                                  message='Please input valid number')],
                                  render_kw={'placeholder': 'Expected stock'})
    received_stock = IntegerField(validators=[InputRequired(),
                                  NumberRange(min=1, max=100,
                                  message='Please input valid number')])
    unit_of_measurement = StringField()

from flask_mongoengine import MongoEngine
from flask_user import UserMixin
import datetime


db = MongoEngine()


class User(db.Document, UserMixin):
    name = db.StringField(default='')
    username = db.StringField()
    # email = db.EmailField(required=True, unique=True)
    password = db.StringField()
    company_name = db.StringField()
    signup_date = db.DateTimeField(default=datetime.datetime.utcnow)
    roles = db.ListField(db.StringField(), default=[])
    pin = db.IntField(default=1010)
    active = db.BooleanField(default=True)


class Category(db.Document):
    category_name = db.StringField()
    company_id = db.ReferenceField('User')


class Supplier(db.Document):
    supplier_name = db.StringField()
    contact_person = db.StringField()
    address = db.StringField()
    phone = db.IntField()
    email = db.EmailField()
    company_id = db.ReferenceField('User')


class Stock(db.Document):
    current_stock = db.IntField()
    stock_change = db.IntField()
    date = db.DateTimeField()
    product_id = db.ReferenceField('Product')


class Product(db.Document):
    name = db.StringField(unique=True)
    category_id = db.ReferenceField('Category')
    brand = db.StringField()
    supplier_id = db.ReferenceField('Supplier')
    unit_of_measurement = db.StringField()
    min_stock_allowed = db.IntField()
    current_stock = db.IntField()
    stock_change = db.IntField()
    company_id = db.ReferenceField('User')

    def update_stock(self, stock_change):
        self.current_stock += stock_change
        self.stock_change += stock_change


class PendingStock(db.Document):
    supplier_id = db.ReferenceField('Supplier')
    delivery_date = db.DateField()
    created_date = db.DateField(default=datetime.datetime.now)
    created_by = db.ReferenceField('User')
    product_list = db.ListField()

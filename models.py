from flask_mongoengine import MongoEngine
from flask_user import UserMixin
import datetime


db = MongoEngine()


class User(db.Document, UserMixin):
    name = db.StringField(default='')
    username = db.StringField()
    email = db.EmailField()
    email_confirmed_at = db.DateTimeField()
    password = db.StringField()
    company_name = db.StringField(default='WokBar')
    roles = db.ListField(db.StringField(), default=['staff'])
    active = db.BooleanField(default=True)


class Category(db.Document):
    category_name = db.StringField()


class Supplier(db.Document):
    supplier_name = db.StringField()
    contact_person = db.StringField()
    address = db.StringField()
    phone = db.IntField()
    email = db.EmailField()


class Product(db.Document):
    name = db.StringField(unique=True, required=True)
    category_id = db.ReferenceField('Category', required=True)
    brand = db.StringField()
    supplier_id = db.ReferenceField('Supplier', required=True)
    unit_of_measurement = db.StringField(required=True)
    min_stock_allowed = db.IntField(required=True)
    current_stock = db.IntField(default=0)
    stock_change = db.IntField(default=0)
    stock_change_date = db.DateTimeField(default=datetime.datetime.now)

    def update_stock(self, stock_change):
        # reset stock_change every new day in order to accumulate stock_change
        # that is made today
        if self.stock_change_date.date() != datetime.datetime.now().date():
            self.stock_change_date = datetime.datetime.now().date()
            self.stock_change = 0
            self.stock_change += stock_change
        else:
            self.current_stock += stock_change
            self.stock_change += stock_change


class PendingStock(db.Document):
    supplier_id = db.ReferenceField('Supplier')
    delivery_date = db.DateField()
    created_date = db.DateField(default=datetime.datetime.now)
    created_by = db.ReferenceField('User')
    product_list = db.ListField()
    is_approved = db.BooleanField(default=False)

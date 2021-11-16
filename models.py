from flask_mongoengine import MongoEngine
from flask_user import UserMixin
import datetime


db = MongoEngine()


class Business(db.Document):
    business_name = db.StringField(required=True)
    business_owner = db.ReferenceField('User')


class User(db.Document, UserMixin):
    name = db.StringField()
    email = db.EmailField()
    email_confirmed_at = db.DateTimeField()
    password = db.StringField()
    business_name = db.StringField()
    roles = db.ListField(db.StringField(), default=['staff'])
    active = db.BooleanField(default=True)
    business_id = db.ReferenceField('Business')
    account_holder = db.BooleanField(default=False)


class Category(db.Document):
    category_name = db.StringField()
    business_id = db.ReferenceField('Business')


class Supplier(db.Document):
    supplier_name = db.StringField()
    contact_person = db.StringField(default='')
    address = db.StringField(default='')
    phone = db.IntField(default=0)
    email = db.StringField(default='')
    business_id = db.ReferenceField('Business')


class Product(db.Document):
    name = db.StringField(required=True)
    category_id = db.ReferenceField('Category')
    brand = db.StringField(default='')
    supplier_id = db.ReferenceField('Supplier')
    unit_of_measurement = db.StringField(required=True)
    min_stock_allowed = db.IntField(required=True)
    current_stock = db.IntField(default=0)
    stock_change = db.IntField(default=0)
    stock_change_date = db.DateTimeField(default=datetime.datetime.now)
    business_id = db.ReferenceField('Business')

    def validate_stock_change(self, stock_change):
        '''Validate that current_stock doesn't go below 0 after stock update'''
        validated_stock = self.current_stock + stock_change

        if validated_stock < 0:
            return False

        return True

    def update_stock(self, stock_change):
        # reset stock_change every new day in order to accumulate stock_change
        # that is made today
        if self.stock_change_date.date() != datetime.datetime.now().date():
            self.stock_change_date = datetime.datetime.now().date()
            self.stock_change = 0
            self.current_stock += stock_change
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
    business_id = db.ReferenceField('Business')

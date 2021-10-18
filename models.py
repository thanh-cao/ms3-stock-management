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

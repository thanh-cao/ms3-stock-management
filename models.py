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
    roles = db.ListField(db.StringField(), default=['staff'])
    pin = db.IntField(default=1010)
    active = db.BooleanField(default=True)

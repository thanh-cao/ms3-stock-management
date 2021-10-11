from flask_mongoengine import MongoEngine
from flask_user import UserMixin
import datetime


db = MongoEngine()
# field choices
USER_ROLE = ('admin', 'staff')


class Access(db.EmbeddedDocument):
    username = db.StringField(required=True)
    pin = db.IntField(required=True, length=4)
    role = db.StringField(required=True, choices=USER_ROLE)


class Account(db.Document, UserMixin):
    name = db.StringField(default='')
    username = db.StringField()
    # email = db.EmailField(required=True, unique=True)
    password = db.StringField()
    company_name = db.StringField()
    signup_date = db.DateTimeField(default=datetime.datetime.utcnow)
    user_access = db.EmbeddedDocumentField(Access)
    active = db.BooleanField(default=True)

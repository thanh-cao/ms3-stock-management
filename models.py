from app import db
import datetime


USER_ROLE = ('admin', 'staff')


class User(db.EmbeddedDocument):
    username = db.StringField(required=True)
    pin = db.IntField(required=True, length=4)
    role = db.StringField(required=True, choices=USER_ROLE)


class Account(db.Document):
    name = db.StringField(minlength=5, maxlength=30)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    company_name = db.StringField(required=True)
    signup_date = db.DateTimeField(default=datetime.datetime.utcnow)
    user_access = db.ListField(db.EmbeddedDocumentField(User, required=True))

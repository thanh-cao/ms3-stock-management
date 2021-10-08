from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Email, Length
import email_validator


class signupForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[
        DataRequired(), Email(granular_message=True)])
    password = PasswordField('Password',
                            [InputRequired(message='You must provide a password!'),
                            Length(min=6, max=20, message='Your password must be between 6 and 20 characters long!')])
    company_name = StringField(label='Company\'s Name')
    submit = SubmitField(label='Sign Up')


class loginForm(FlaskForm):
    email = StringField(label='Email', validators=[
        DataRequired(), Email(granular_message=True)])
    password = PasswordField('Password',
                            [InputRequired(message='You must provide a password!'),
                            Length(min=6, max=20, message='Your password must be between 6 and 20 characters long!')])
    submit = SubmitField(label='Log In')

import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_mongoengine import MongoEngine
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from models import *
from forms import *
if os.path.exists('env.py'):
    import env

# set up Flask app and config
app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': os.environ.get('MONGO_DBNAME'),
    'host': os.environ.get('MONGO_URI'),
}
app.secret_key = os.environ.get('SECRET_KEY')
# set up Flask-Mongoengine connection to connect to MongoDB
db = MongoEngine(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = signupForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # Check if account already exists in database
            existing_account = Account.objects(email=form.email.data).first()
            if existing_account:
                flash("Email already registered!")
                return redirect(url_for('signup'))

            # Gather new account registration info and save to database
            password = generate_password_hash(form.password.data)
            admin_user = User(username=form.name.data,
                              pin=1010,
                              role='admin')
            new_account = Account(name=form.name.data,
                                  email=form.email.data,
                                  password=password,
                                  company_name=form.company_name.data,
                                  user_access=admin_user)
            new_account.save()

            session['account'] = form.name.data
            return redirect(url_for('profile', name=session['account']))
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm()
    if request.method == 'POST':
        # Check if account exists in database
        existing_account = Account.objects(email=form.name.data).first()
        password = form.password.data

        if existing_account:
            # Check if hashed password matches user input
            if check_password_hash(existing_account['password'], password):
                session['account'] = form.name.data
                return redirect(url_for('profile', name=session['account']))
            else:
                # invalid password
                flash('Incorrect Password')
                return redirect(url_for('login'))
        else:
            # username doesn't exist
            flash('Incorrect Username')
            print('check password')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/profile')
def profile():
    return render_template('profile.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)

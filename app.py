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
            existing_account = Account.objects(email=form.email.data).first()
            if existing_account:
                # flash("Email already registered!")
                return redirect(url_for('signup'))

            password = generate_password_hash(form.password.data)
            admin_user = User(username=form.name.data,
                            role='admin')
            new_account = Account(name=form.name.data,
                            email=form.email.data,
                            password=password,
                            company_name=form.company_name.data,
                            user_access=admin_user)
            new_account.save()
            return redirect(url_for('index'))
    return render_template('signup.html', form=form)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)

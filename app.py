import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_mongoengine import MongoEngine
from flask_wtf.csrf import CSRFProtect
from flask_user import login_required, current_user, roles_required
from flask_user.signals import user_registered
from flask_login import logout_user
from bson.objectid import ObjectId
from models import *
from forms import *
from config import ConfigClass
if os.path.exists('env.py'):
    import env


# Set up Flask app and config
app = Flask(__name__)
app.config.from_object(__name__ + '.ConfigClass')

# Set up Flask-Mongoengine connection to connect to MongoDB
db = MongoEngine(app)
# Set up WTForms CSRFProtect
csrf = CSRFProtect()
csrf.init_app(app)
# Setup Flask-User with customized registration form
user_manager = CustomUserManager(app, db, User)


@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    return render_template('index.html')


# create default super_admin role upon registration to account holder/owner
@user_registered.connect_via(app)
def create_super_admin(sender, user, **extra):
    user.roles.append('super_admin')
    user.save()


@app.route('/profile/', methods=['GET', 'POST'])
@login_required
@roles_required('super_admin')
def profile():
    account = current_user
    account_form = CustomRegisterForm()
    access_form = UserAccess()
    return render_template('profile.html',
                           account=account,
                           account_form=account_form,
                           access_form=access_form)


@app.route('/profile/edit/<account_id>', methods=['GET', 'POST'])
@login_required
@roles_required('super_admin')
def edit_profile(account_id):
    account = User.objects.get(id=account_id)
    if request.method == 'POST':
        updated_profile = {
            'name': request.form.get('name'),
            'company_name': request.form.get('company_name')
        }
        account.update(**updated_profile)
        flash('Profile successfully updated')
        return redirect(url_for('profile'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)

import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_mongoengine import MongoEngine
from mongoengine.queryset.visitor import Q
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

#############################
### Profile / User access ###
#############################
@app.route('/profile')
@login_required
@roles_required('super_admin')
def profile():
    account = current_user
    user_access = User.objects(Q(roles='admin') | Q(roles='staff'))
    account_form = CustomRegisterForm()
    access_form = UserAccess()
    return render_template('profile.html',
                           account=account,
                           user_access=user_access,
                           account_form=account_form,
                           access_form=access_form)


@app.route('/profile/edit/<account_id>', methods=['POST'])
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


@app.route('/profile/create_accesss', methods=['POST'])
@login_required
@roles_required('super_admin')
def create_access():
    company = current_user.company_name
    if request.method == 'POST':
        access = User(
            username=request.form.get('username'),
            pin=request.form.get('pin'),
            company_name=company,
            roles=[request.form.get('role')]
            )
        access.save()
        flash('New user access successfully updated')
        return redirect(url_for('profile'))


@app.route('/profile/edit_accesss/<access_id>', methods=['POST'])
@login_required
@roles_required('super_admin')
def edit_accesss(access_id):
    access = User.objects.get(id=access_id)
    access.roles.pop()
    if request.method == 'POST':
        new_role = request.form.get('role')
        access.roles.append(new_role)
        updated_access = {
            'username': request.form('username'),
            'pin': request.form('pin'),
        }
        access.update(**updated_access)
        flash('Access successfully updated')
        return redirect(url_for('profile'))


#############################
##### Product category ######
#############################

@app.route('/categories')
@login_required
def categories():
    category_form = CategoryForm()
    categories = Category.objects()
    return render_template('categories.html', categories=categories, form=category_form)


@app.route('/categories/create', methods=['POST'])
@login_required
def create_category():
    if request.method == 'POST':
        new_category = Category(category_name=request.form.get('category_name'))
        new_category.save()
        return redirect(url_for('categories'))


@app.route('/categories/delete/<category_id>')
@login_required
def delete_category(category_id):
    category = Category.objects.get(id=category_id)
    category.delete()
    return redirect(url_for('categories'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)

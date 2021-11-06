import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, jsonify)
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


# Create default super_admin role upon registration to account holder/owner
@user_registered.connect_via(app)
def create_super_admin(sender, user, **extra):
    user.roles.append('super_admin')
    user.save()


# Routes for Profile / User access
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
def get_categories():
    form = CategoryForm()
    categories = Category.objects()
    return render_template('categories.html', categories=categories, form=form)


@app.route('/categories/create', methods=['POST'])
@login_required
def create_category():
    if request.method == 'POST':
        new_category = Category(
            category_name=request.form.get('category_name'))
        new_category.save()
        return redirect(url_for('get_categories'))


@app.route('/edit_category/<category_id>', methods=['POST'])
@login_required
def edit_category(category_id):
    category = Category.objects.get(id=category_id)
    if request.method == 'POST':
        edit = {
            'category_name': request.form.get('category_name')
        }
        category.update(**edit)
        return redirect(url_for('get_categories'))


@app.route('/categories/delete/<category_id>')
@login_required
def delete_category(category_id):
    category = Category.objects.get(id=category_id)
    category.delete()
    return redirect(url_for('get_categories'))


#############################
######## Suppliers ##########
#############################


@app.route('/suppliers')
def get_suppliers():
    suppliers = Supplier.objects()
    form = SupplierForm()
    return render_template('suppliers.html', suppliers=suppliers, form=form)


@app.route('/suppliers/create', methods=['POST'])
@login_required
def create_supplier():
    if request.method == 'POST':
        new_supplier = Supplier(
            supplier_name=request.form.get('supplier_name'),
            contact_person=request.form.get('contact_person'),
            address=request.form.get('address'),
            phone=request.form.get('phone'),
            email=request.form.get('email'))
        new_supplier.save()
        return redirect(url_for('get_suppliers'))


@app.route('/edit_supplier/<supplier_id>', methods=['POST'])
@login_required
def edit_supplier(supplier_id):
    supplier = Supplier.objects.get(id=supplier_id)
    if request.method == 'POST':
        edit = {
            'supplier_name': request.form.get('supplier_name'),
            'contact_person': request.form.get('contact_person'),
            'address': request.form.get('address'),
            'phone': request.form.get('phone'),
            'email': request.form.get('email')
        }
        supplier.update(**edit)
        return redirect(url_for('get_suppliers'))


@app.route('/suppliers/delete/<supplier_id>')
@login_required
def delete_supplier(supplier_id):
    supplier = Supplier.objects.get(id=supplier_id)
    supplier.delete()
    return redirect(url_for('get_suppliers'))


#############################
######### Products ##########
#############################


@app.route('/products')
@login_required
def get_products():
    # Create new product form and choices for select fields
    form = ProductForm()
    categories = Category.objects()
    suppliers = Supplier.objects()
    products = Product.objects()
    form.category_id.choices = [(category.id, category.category_name)
                                for category in categories]
    form.supplier_id.choices = [(supplier.id, supplier.supplier_name)
                                for supplier in suppliers]
    today = datetime.datetime.now().date()  # to find stock_change for today
    return render_template('products.html',
                           products=products,
                           categories=categories,
                           form=form, today=today)


@app.route('/products/create', methods=['POST'])
@login_required
def create_product():
    if request.method == 'POST':
        new_product = Product(
            name=request.form.get('name'),
            category_id=request.form.get('category_id'),
            brand=request.form.get('brand'),
            supplier_id=request.form.get('supplier_id'),
            unit_of_measurement=request.form.get('unit_of_measurement'),
            min_stock_allowed=request.form.get('min_stock_allowed'),
            current_stock=request.form.get('current_stock'))
        new_product.save()

        flash('New product successfully created')
        return redirect(url_for('get_products'))


@app.route('/products/<product_id>')
@login_required
def product_details(product_id):
    form = ProductForm()
    categories = Category.objects()
    suppliers = Supplier.objects()
    form.category_id.choices = [(category.id, category.category_name)
                                for category in categories]
    form.supplier_id.choices = [(supplier.id, supplier.supplier_name)
                                for supplier in suppliers]
    product = Product.objects.get(id=product_id)
    today = datetime.datetime.now().date()
    return render_template('product-details.html', product=product,
                           form=form, today=today)


@app.route('/products/edit/<product_id>', methods=['POST'])
@login_required
def edit_product(product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        edit = {
            'name': request.form.get('name'),
            'category_id': ObjectId(request.form.get('category_id')),
            'brand': request.form.get('brand'),
            'supplier_id': ObjectId(request.form.get('supplier_id')),
            'unit_of_measurement': request.form.get('unit_of_measurement'),
            'min_stock_allowed': request.form.get('min_stock_allowed')
        }
        product.update(**edit)
        flash('Product successfully updated')
        return redirect(url_for('product_details', product_id=product_id))


@app.route('/products/delete/<product_id>')
@login_required
def delete_product(product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    flash('Product is deleted')
    return redirect(url_for('get_products'))


@app.route('/update_stock/<product_id>', methods=['POST'])
@login_required
def update_stock(product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        stock_change = int(request.form.get('stock_change'))
        product.update_stock(stock_change)
        product.save()
        flash('Stock successfully updated')
        return redirect(request.referrer)


#############################
######## Dashboard ##########
#############################


@app.route('/dashboard')
@login_required
def dashboard():
    products = Product.objects()
    pending_stocks = PendingStock.objects()

    # Create a list of products that need to be restocked now
    # and products with stock change today
    restocks = []
    stock_change_product = []
    for product in products:
        if product.current_stock <= product.min_stock_allowed:
            restocks.append(product)
        if product.stock_change_date.date() == datetime.datetime.now().date():
            stock_change_product.append(product)

    # If there's a session previously created from abandoned process of
    # creating new, editting pending stock form or updating stock, it should
    # be cleared for new actions
    for item in ['pending', 'stock']:
        if item in session:
            session.pop(item)

    return render_template('dashboard.html',
                           stock_change_product=stock_change_product,
                           restocks=restocks,
                           pending_stocks=pending_stocks)


@app.route('/pending-stock/create', methods=['GET', 'POST'])
@login_required
def create_pending_stock():
    form = PendingStockForm()  # the main form to be saved in database
    product_form = AddProduct()  # add products to pending stock form
    products = Product.objects()  # populate type ahead suggestions
    suppliers = Supplier.objects()
    form.supplier_id.choices = [(supplier.id, supplier.supplier_name)
                                for supplier in suppliers]

    if form.validate_on_submit():
        if 'pending' not in session:
            flash('Please add products to your pending stock form')
            return redirect(request.referrer)
        product_list = session['pending']
        pending_stock = PendingStock(
                        supplier_id=form.supplier_id.data,
                        delivery_date=form.delivery_date.data,
                        created_date=datetime.datetime.now().date(),
                        created_by=current_user.id,
                        product_list=product_list)
        pending_stock.save()
        session.pop('pending')
        return redirect(url_for('dashboard'))

    return render_template('create-pending-stock.html', form=form,
                           products=products,
                           product_form=product_form)


@app.route('/add-pending-product', methods=['POST'])
@login_required
def add_product_to_pending_stock():
    '''
    Create a session object called 'pending' and add products into the session
    which is then later parsed to pending stock form to be saved in database
    '''
    if 'pending' not in session:
        session['pending'] = []

    form = AddProduct()
    session['pending'].append(
                          {'id': form.id.data,
                           'name': form.name.data,
                           'expected_stock': form.expected_stock.data,
                           'unit_of_measurement': form.unit_of_measurement.data
                           })
    session.modified = True
    return redirect(request.referrer)


@app.route('/remove-pending-product/<id>')
@login_required
def remove_product_from_pending_stock(id):
    '''
    Find matching item from session 'pending' based on item's id and remove it
    '''
    for item in session['pending']:
        if item['id'] == id:
            session['pending'].remove(item)
            session.modified = True
    return redirect(request.referrer)


@app.route('/pending-stock/<id>')
@login_required
def pending_stock_details(id):
    '''
    Detailed view for pending stock. A 'pending' session is also created
    with product list in the pending stock to be used
    later if user wants to edit pending stock form
    '''
    pending = PendingStock.objects.get(id=id)
    session['pending'] = pending.product_list
    form = AddProduct()

    return render_template('pending-stock-details.html',
                           pending=pending,
                           form=form)


@app.route('/pending-stock/delete/<id>')
@login_required
def delete_pending_stock(id):
    '''
    Delete chosen pending stock
    '''
    pending = PendingStock.objects.get(id=id)
    pending.delete()
    return redirect(url_for('dashboard'))


@app.route('/pending-stock/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_pending_stock(id):
    '''
    Edit chosen pending stock. Session 'pending' which is created
    on pending stock detailed view, is used to populate product list
    '''
    pending_stock = PendingStock.objects.get(id=id)
    form = PendingStockForm()
    product_form = AddProduct()
    products = Product.objects()  # populate type ahead suggestions

    if request.method == 'POST':
        if len(session['pending']) == 0:
            flash('Please add products to your pending stock form')
            return redirect(request.referrer)
        product_list = session['pending']
        edit = {'delivery_date': form.delivery_date.data,
                'created_date': datetime.datetime.now().date(),
                'created_by': ObjectId(current_user.id),
                'product_list': product_list}
        pending_stock.update(**edit)
        session.pop('pending')
        flash('Pending stock form updated successfully')
        return redirect(url_for('pending_stock_details', id=id))

    return render_template('edit-pending-stock.html',
                           pending_stock=pending_stock,
                           products=products,
                           form=form,
                           product_form=product_form)


@csrf.exempt
@app.route('/pending-stock/update', methods=['POST'])
def update_pending_stock():
    '''
    When user inputs the number of stock received upon stock delivery,
    the change is stored in session 'stock' in order to prepare data
    before stock change is actually updated in the database when user
    clicks approve
    '''
    if 'stock' not in session:
        session['stock'] = []

    for item in session['stock']:
        if item['id'] == request.form['id']:
            item.update({'received_stock': request.form['received_stock']})
            return jsonify(session['stock'])

    session['stock'].append({'id': request.form['id'],
                             'received_stock': request.form['received_stock']})
    session.modified = True
    print(f"after added {session['stock']}")
    return jsonify(session['stock'])


@app.route('/pending-stock/approve/<id>')
@login_required
def approve_pending_stock(id):
    '''
    When user approves stock received, product list in pending stock is
    updated with received stock. After that, stock update is done for each
    product based on their product's ID. Status of the pending stock is
    changed to 'done' and after that user cannot made any further change
    to the pending stock.
    '''
    pending_stock = PendingStock.objects.get(id=id)

    for pending_product in pending_stock.product_list:
        for item in session['stock']:
            if item['id'] == pending_product['id']:
                pending_product['received_stock'] = item['received_stock']

        product = Product.objects.get(id=pending_product['id'])
        product.update_stock(int(item['received_stock']))
        product.save()

    pending_stock.is_approved = True
    pending_stock.save()
    session.pop('stock')
    return redirect(request.referrer)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)

import os
import json
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, jsonify)
from flask_mongoengine import MongoEngine
from mongoengine.queryset.visitor import Q
from flask_wtf.csrf import CSRFProtect
from flask_user import login_required, current_user, roles_required
from flask_user.signals import user_registered
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
    '''
    Create view for index page. If a user is already logged in,
    redirect to dashboard
    '''
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    # Get json data for feature section on index page
    features = []
    testimonials = []
    with open('data/features.json', 'r') as features_data:
        features = json.load(features_data)
    with open('data/testimonials.json', 'r') as testimonials_data:
        testimonials = json.load(testimonials_data)

    return render_template('index.html', features=features,
                           testimonials=testimonials)


@user_registered.connect_via(app)
def create_business(sender, user, **extra):
    '''
    Create new business in database and admin role
    upon registration to account holder/owner
    '''
    existing_business = Business.objects(
                                 business_name=user.business_name).first()
    if not existing_business:
        business = Business(business_name=user.business_name,
                            business_owner=user.id)
        business.save()
        user.business_id = business.id
        user.account_holder = True
        user.roles.pop()
        user.roles.append('admin')
        user.save()


@app.route('/account')
@login_required
@roles_required('admin')
def account():
    '''
    Create view for account page with forms to edit account,
    create new user access, edit user access, and delete user access
    '''
    account = current_user
    user_access = User.objects(Q(business_id=account.business_id) &
                               Q(roles='admin') | Q(roles='staff'))
    account_form = CustomRegisterForm()
    access_form = UserAccess()
    return render_template('account.html',
                           account=account,
                           user_access=user_access,
                           account_form=account_form,
                           access_form=access_form)


@app.route('/account/edit/<account_id>', methods=['POST'])
@login_required
@roles_required('admin')
def edit_account(account_id):
    '''
    Edit account of account holder/owner
    '''
    account = User.objects.get(id=account_id)
    business = Business.objects.get(id=account.business_id.id)
    if request.method == 'POST':
        updated_account = {
            'name': request.form.get('name'),
            'business_name': request.form.get('business_name')
        }
        account.update(**updated_account)
        business.update(business_name=request.form.get('business_name'))
        flash('Account successfully updated', 'success')
        return redirect(url_for('account'))


@app.route('/account/create_access', methods=['POST'])
@login_required
@roles_required('admin')
def create_new_access():
    '''
    Create new user access for staff with either staff of admin role
    '''
    form = UserAccess()
    password = form.password.data
    hashed_password = user_manager.hash_password(password)
    if form.validate_on_submit():
        new_access = User(name=form.name.data,
                          email=form.email.data,
                          email_confirmed_at=datetime.datetime.now(),
                          password=hashed_password,
                          roles=[form.roles.data],
                          business_id=current_user.business_id)
        new_access.save()
        flash('New user access successfully created', 'success')
        return redirect(url_for('account'))

    for field_errors in form.errors.values():
        for error in field_errors:
            flash(error, 'error')
    return redirect(url_for('account'))


@app.route('/edit_user_access/<access_id>', methods=['POST'])
@login_required
@roles_required('admin')
def edit_access(access_id):
    '''
    Edit user access for staff with either staff of admin role
    '''
    access = User.objects.get(id=access_id)
    new_role = request.form.get('roles')

    access.roles = [new_role]
    access.name = request.form.get('name')
    access.save()

    flash('Access successfully updated', 'success')
    return redirect(url_for('account'))


@app.route('/account/delete_access/<access_id>')
@login_required
@roles_required('admin')
def delete_access(access_id):
    '''
    Delete user access for staff with either staff of admin role
    '''
    access = User.objects.get(id=access_id)
    access.delete()
    flash('Access successfully deleted', 'success')
    return redirect(url_for('account'))


@csrf.exempt
@app.route('/account/query', methods=['POST'])
@login_required
def query_account_collection():
    '''
    Route to receive query call from frontend and return the data
    to use in scripts.js in order to prepopulate the frontend forms with
    edit functionality
    '''
    id = request.form.get('ObjectId')
    data = User.objects(id=id, business_id=current_user.business_id).first()
    return jsonify(data)


# This section below contains functions and routes related to categories #


@app.route('/categories')
@roles_required('admin')
@login_required
def get_categories():
    '''
    Create view for categories page with forms to create new / edit category
    '''
    form = CategoryForm()
    categories = Category.objects(business_id=current_user.business_id)
    return render_template('categories.html', categories=categories, form=form)


@app.route('/categories/create', methods=['POST'])
@roles_required('admin')
@login_required
def create_category():
    '''
    Route to create new category
    '''
    form = CategoryForm()
    if form.validate_on_submit():
        new_category = Category(
            category_name=request.form.get('category_name'),
            business_id=current_user.business_id)
        new_category.save()
        flash('Category successfully created', 'success')
        return redirect(url_for('get_categories'))

    for field_errors in form.errors.values():
        for error in field_errors:
            flash(error, 'error')
    return redirect(url_for('get_categories'))


@app.route('/edit_category/<category_id>', methods=['POST'])
@login_required
@roles_required('admin')
def edit_category(category_id):
    '''
    Route to edit category
    '''
    category = Category.objects.get(id=category_id)
    form = CategoryForm()
    if form.validate_on_submit():
        edit = {
            'category_name': request.form.get('category_name')
        }
        category.update(**edit)
        flash('Category successfully updated', 'success')
        return redirect(url_for('get_categories'))

    for field_errors in form.errors.values():
        for error in field_errors:
            flash(error, 'error')
    return redirect(url_for('get_categories'))


@app.route('/categories/delete/<category_id>')
@login_required
@roles_required('admin')
def delete_category(category_id):
    '''
    Route to delete category
    '''
    category = Category.objects.get(id=category_id)
    category.delete()
    flash('Category successfully deleted', 'success')
    return redirect(url_for('get_categories'))


@csrf.exempt
@app.route('/category/query', methods=['POST'])
@login_required
def query_category_collection():
    '''
    Route to receive query call from frontend and return the data
    to use in scripts.js in order to prepopulate the frontend forms with
    edit functionality
    '''
    id = request.form.get('ObjectId')
    data = Category.objects(id=id,
                            business_id=current_user.business_id).first()
    return jsonify(data)


# This section below contains functions and routes related to suppliers #


@app.route('/suppliers')
def get_suppliers():
    '''
    Create view for suppliers page with forms to create new / edit supplier
    '''
    suppliers = Supplier.objects(business_id=current_user.business_id)
    form = SupplierForm()
    return render_template('suppliers.html', suppliers=suppliers, form=form)


@app.route('/suppliers/create', methods=['POST'])
@roles_required('admin')
@login_required
def create_supplier():
    '''
    Route to create new supplier
    '''
    form = SupplierForm()
    if form.validate_on_submit():
        new_supplier = Supplier(
            supplier_name=request.form.get('supplier_name'),
            contact_person=request.form.get('contact_person'),
            address=request.form.get('address'),
            phone=request.form.get('phone'),
            email=request.form.get('email'),
            business_id=current_user.business_id)
        new_supplier.save()
        flash('Supplier successfully created', 'success')
        return redirect(url_for('get_suppliers'))

    for field_errors in form.errors.values():
        for error in field_errors:
            flash(error, 'error')
    return redirect(url_for('get_suppliers'))


@app.route('/edit_supplier/<supplier_id>', methods=['POST'])
@roles_required('admin')
@login_required
def edit_supplier(supplier_id):
    '''
    Route to edit supplier
    '''
    supplier = Supplier.objects.get(id=supplier_id)
    form = SupplierForm()
    if form.validate_on_submit():
        edit = {
            'supplier_name': request.form.get('supplier_name'),
            'contact_person': request.form.get('contact_person'),
            'address': request.form.get('address'),
            'phone': request.form.get('phone'),
            'email': request.form.get('email')
        }
        supplier.update(**edit)
        flash('Supplier successfully updated', 'success')
        return redirect(url_for('get_suppliers'))

    for field_errors in form.errors.values():
        for error in field_errors:
            flash(error, 'error')
    return redirect(url_for('get_suppliers'))


@app.route('/suppliers/delete/<supplier_id>')
@roles_required('admin')
@login_required
def delete_supplier(supplier_id):
    '''
    Route to delete supplier
    '''
    supplier = Supplier.objects.get(id=supplier_id)
    supplier.delete()
    flash('Supplier successfully deleted', 'success')
    return redirect(url_for('get_suppliers'))


@csrf.exempt
@app.route('/supplier/query', methods=['POST'])
@login_required
def query_supplier_collection():
    '''
    Route to receive query call from frontend and return the data
    to use in scripts.js in order to prepopulate the frontend forms with
    edit functionality
    '''
    id = request.form.get('ObjectId')
    data = Supplier.objects(id=id,
                            business_id=current_user.business_id).first()
    return jsonify(data)


# This section below contains functions and route related to products #


def create_category_choices(field):
    '''
    Query the database for all categories and create a list of tuples
    in order to populate dynamic options for select field
    '''
    categories = Category.objects(business_id=current_user.business_id)
    category_choices = [(category.id, category.category_name)
                        for category in categories]
    field.choices = category_choices
    return field.choices


def create_supplier_choices(field):
    '''
    Query the database for all suppliers and create a list of tuples
    in order to populate dynamic options for select field
    '''
    suppliers = Supplier.objects(business_id=current_user.business_id)
    supplier_choices = [(supplier.id, supplier.supplier_name)
                        for supplier in suppliers]
    field.choices = supplier_choices
    return field.choices


def create_product_form():
    '''
    Create ProductForm and add dynamic choices to the form
    '''
    form = ProductForm()
    create_category_choices(form.category_id)
    create_supplier_choices(form.supplier_id)
    return form


@app.route('/products')
@login_required
def get_products():
    '''
    Create view for products page categorized by categories
    with forms to create new product
    '''
    # Create new product form and choices for select fields
    form = create_product_form()

    categories = Category.objects(business_id=current_user.business_id)
    products = Product.objects(business_id=current_user.business_id)
    today = datetime.datetime.now().date()  # to find stock_change for today

    return render_template('products.html',
                           products=products,
                           categories=categories,
                           form=form, today=today)


@app.route('/products/create', methods=['POST'])
@roles_required('admin')
@login_required
def create_product():
    '''
    Route to create new product
    '''
    form = create_product_form()

    if form.validate_on_submit():
        new_product = Product(
            name=request.form.get('name'),
            category_id=request.form.get('category_id'),
            brand=request.form.get('brand'),
            supplier_id=request.form.get('supplier_id'),
            unit_of_measurement=request.form.get('unit_of_measurement'),
            min_stock_allowed=request.form.get('min_stock_allowed'),
            current_stock=request.form.get('current_stock'),
            business_id=current_user.business_id)
        new_product.save()

        flash('New product successfully created', 'success')
        return redirect(url_for('get_products'))

    for field_errors in form.errors.values():
        for error in field_errors:
            flash(error, 'error')
    return redirect(url_for('get_products'))


@app.route('/products/<product_id>')
@login_required
def product_details(product_id):
    '''
    Create view to display product details and form to edit details
    '''
    form = create_product_form()
    product = Product.objects.get(id=product_id)
    today = datetime.datetime.now().date()

    return render_template('product-details.html', product=product,
                           form=form, today=today)


@app.route('/products/edit/<product_id>', methods=['POST'])
@roles_required('admin')
@login_required
def edit_product(product_id):
    '''
    Route to edit product
    '''
    product = Product.objects.get(id=product_id)
    form = create_product_form()

    if form.validate_on_submit():
        edit = {
            'name': request.form.get('name'),
            'category_id': ObjectId(request.form.get('category_id')),
            'brand': request.form.get('brand'),
            'supplier_id': ObjectId(request.form.get('supplier_id')),
            'unit_of_measurement': request.form.get('unit_of_measurement'),
            'min_stock_allowed': request.form.get('min_stock_allowed')
        }
        product.update(**edit)
        flash('Product successfully updated', 'success')
        return redirect(url_for('product_details', product_id=product_id))

    for field_errors in form.errors.values():
        for error in field_errors:
            flash(error, 'error')
    return redirect(url_for('product_details', product_id=product_id))


@app.route('/products/delete/<product_id>')
@roles_required('admin')
@login_required
def delete_product(product_id):
    '''
    Route to delete product
    '''
    product = Product.objects.get(id=product_id)
    product.delete()
    flash('Product is deleted', 'success')
    return redirect(url_for('get_products'))


@app.route('/edit_product_stock/<product_id>', methods=['POST'])
@login_required
def update_stock(product_id):
    '''
    Route to update product stock
    '''
    product = Product.objects.get(id=product_id)
    stock_update = int(request.form.get('stock_update'))

    if product.validate_stock_change(stock_update):
        product.update_stock(stock_update)
        product.save()
        flash('Stock successfully updated', 'success')
        return redirect(request.referrer)

    flash('Stock change cannot be greater than current stock', 'error')
    return redirect(request.referrer)


@csrf.exempt
@app.route('/product/query', methods=['POST'])
@login_required
def search_product():
    '''
    Route to receive search query from the frontend and return the product list
    to use in search.js and typeahead.js
    '''
    query = request.form.get('query')
    filtered = Product.objects(name__icontains=query,
                               business_id=current_user.business_id)
    if query == 'all':
        filtered = Product.objects(business_id=current_user.business_id)

    if query == 'supplier':
        supplier_id = request.form.get('supplier_id')
        filtered = Product.objects(supplier_id=supplier_id,
                                   business_id=current_user.business_id)
    if query == 'product':
        product_id = request.form.get('ObjectId')
        filtered = Product.objects(id=product_id,
                                   business_id=current_user.business_id
                                   ).first()
    return jsonify(filtered)


# This section below contains routes related to dashboard and pending stock #


@app.route('/dashboard')
@login_required
def dashboard():
    '''
    Dashboard shows 3 sections: Restock now shows products that have reached
    minimum stock level. Pending stock shows incoming deliveries. Stock update
    shows products that have stock change today, and search bar to allow quick
    search for products to do stock update right on dashboard.
    '''
    form = ProductForm()
    products = Product.objects(business_id=current_user.business_id)

    # Show incoming pending stocks dated 7 days back
    historic_date = datetime.datetime.now().date() - datetime.timedelta(days=7)
    pending_stocks = PendingStock.objects(business_id=current_user.business_id,
                                          delivery_date__gt=historic_date)
    pending_form = PendingStockForm()  # to create search for pending stocks
    create_supplier_choices(pending_form.supplier_id)

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
                           pending_stocks=pending_stocks,
                           form=form, pending_form=pending_form)


@csrf.exempt
@app.route('/pending-stock/search', methods=['POST'])
@login_required
def search_pending_stock():
    '''
    Route to receive search query from the frontend and return the pending
    stock list to use in search.js to display on dashboard page
    '''
    supplier_id = request.form.get('supplier_id')
    delivery_date = request.form.get('delivery_date')

    if delivery_date == '':
        filtered = PendingStock.objects(supplier_id=supplier_id,
                                        business_id=current_user.business_id)
    else:
        filtered = PendingStock.objects((Q(supplier_id=supplier_id) &
                                        Q(delivery_date=delivery_date)))

    return jsonify(filtered)


@app.route('/pending-stock/create', methods=['GET', 'POST'])
@roles_required('admin')
@login_required
def create_pending_stock():
    '''
    Create view to display form and receive form data
    to create new pending stock
    '''
    form = PendingStockForm()  # the main form to be saved in database
    create_supplier_choices(form.supplier_id)
    product_form = AddProduct()  # add products to pending stock form

    if form.validate_on_submit():
        if 'pending' not in session:
            flash('Please add products to your pending stock form', 'error')
            return redirect(request.referrer)

        product_list = session['pending']
        pending_stock = PendingStock(
                        supplier_id=form.supplier_id.data,
                        delivery_date=form.delivery_date.data,
                        created_date=datetime.datetime.now().date(),
                        created_by=current_user.id,
                        product_list=product_list,
                        business_id=current_user.business_id)
        pending_stock.save()
        session.pop('pending')

        flash('Pending stock successfully created', 'success')
        return redirect(url_for('pending_stock_details', id=pending_stock.id))

    for field_errors in form.errors.values():
        for error in field_errors:
            flash(error, 'error')
    return render_template('create-pending-stock.html', form=form,
                           product_form=product_form)


@app.route('/add-pending-product', methods=['POST'])
@roles_required('admin')
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
@roles_required('admin')
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
@roles_required('admin')
@login_required
def delete_pending_stock(id):
    '''
    Delete chosen pending stock
    '''
    pending = PendingStock.objects.get(id=id)
    pending.delete()
    flash('Pending stock successfully deleted', 'success')
    return redirect(url_for('dashboard'))


@app.route('/pending-stock/edit/<id>', methods=['GET', 'POST'])
@roles_required('admin')
@login_required
def edit_pending_stock(id):
    '''
    Edit chosen pending stock. Session 'pending' which is created
    on pending stock detailed view, is used to populate product list
    '''
    pending_stock = PendingStock.objects.get(id=id)
    form = PendingStockForm()
    product_form = AddProduct()

    if request.method == 'POST':
        if len(session['pending']) == 0:
            flash('Please add products to your pending stock form', 'error')
            return redirect(request.referrer)

        product_list = session['pending']
        edit = {'delivery_date': form.delivery_date.data,
                'created_date': datetime.datetime.now().date(),
                'created_by': ObjectId(current_user.id),
                'product_list': product_list}
        pending_stock.update(**edit)
        session.pop('pending')

        flash('Pending stock form updated successfully', 'success')
        return redirect(url_for('pending_stock_details', id=id))

    return render_template('edit-pending-stock.html',
                           pending_stock=pending_stock,
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

        if product.validate_stock_change(int(item['received_stock'])) is False:
            flash('Stock change is not valid', 'error')
            return redirect(url_for('pending_stock_details', id=id))

        product.update_stock(int(item['received_stock']))
        product.save()

    pending_stock.is_approved = True
    pending_stock.save()
    session.pop('stock')
    flash('Pending stock approved successfully', 'success')
    return redirect(request.referrer)


# Error handlers #


@app.errorhandler(404)
def page_not_found(error):
    '''
    Display error page for 404 error
    '''
    error = 'The page you are looking for could not be found.'
    return render_template('error.html', error=error), 404


@app.errorhandler(500)
def internal_server_error(error):
    '''
    Display error page for 500 error
    '''
    error = 'There was an error on our end. Please try again later.'
    return render_template('error.html', error=error), 500


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=os.environ.get('DEBUG'))

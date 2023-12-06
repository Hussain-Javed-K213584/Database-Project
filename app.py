from flask import Flask, g,  abort, request, render_template, session, flash, redirect,url_for
from flask_login import login_required, logout_user, current_user ,UserMixin, LoginManager, login_user
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from helper import generate_product_code, upload_file
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'super secret!'
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wavy.db'
login_manager = LoginManager(app)
db = SQLAlchemy()
bcrypt = Bcrypt(app)

login_manager.login_view = '/login'

class ProductTable(db.Model):
    __tablename__ = 'Product_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    prod_code = db.Column(db.Integer, nullable=False, unique=True)
    image_path = db.Column(db.String(255))

class Accessories(db.Model):
    __tablename__ = 'Accessories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(100), nullable=False)
    prod_code = db.Column(db.String(50), nullable=False, unique=True)
    product_table_id = db.Column(db.Integer, db.ForeignKey('Product_table.id'), nullable=False)
    product = db.relationship('ProductTable', backref='accessories')
    image_path = db.Column(db.String(255))

class Jeans(db.Model):
    __tablename__ = 'Jeans'

    gender = db.Column(db.String(1), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    qty = db.Column(db.Integer, nullable=False)
    prod_code = db.Column(db.String(50), nullable=False, unique=True)
    product_table_id = db.Column(db.Integer, db.ForeignKey('Product_table.id'), nullable=False)
    product = db.relationship('ProductTable', backref='jeans')
    image_path = db.Column(db.String(255))

class Orders(db.Model):
    __tablename__ = 'Orders'

    id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Integer, nullable=False)
    qty_ordered = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime(timezone=False), nullable=False, default=datetime.now())
    users_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    image_path = image_path = db.Column(db.String(255))
    user = db.relationship('Users', backref='orders')
    
class Shoes(db.Model):
    __tablename__ = 'Shoes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    type = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    prod_code = db.Column(db.String(50), nullable=False, unique=True)
    product_table_id = db.Column(db.Integer, db.ForeignKey('Product_table.id'), nullable=False)
    product = db.relationship('ProductTable', backref='shoes')
    image_path = db.Column(db.String(255))

class Tshirts(db.Model):
    __tablename__ = 'Tshirts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    qty = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    prod_code = db.Column(db.String(50), nullable=False, unique=True)
    product_table_id = db.Column(db.Integer, db.ForeignKey('Product_table.id'), nullable=False)
    product = db.relationship('ProductTable', backref='tshirts')
    image_path = db.Column(db.String(255))

class Users(db.Model, UserMixin):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    Phone_no = db.Column(db.Integer, nullable=False)
    Name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(50), nullable=False)

def admin_only(f):
    @wraps(f)
    def decorated_fun(*args, **kwargs):
        if current_user is None or current_user.id != 1:
            print(current_user.id)
            flash("404 - Does not exists")
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_fun 

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/')
def index():
    base_url = request.url_root
    accessories = Accessories.query.all()
    shirts = Tshirts.query.all()
    shoes = Shoes.query.all()
    jeans = Jeans.query.all()
    for sh in shirts:
        print(sh.name)
    return render_template('index.html', item_list=[accessories, shirts, shoes, jeans], base_url=base_url)

@app.route('/admin-panel')
@admin_only
@login_required
def admin_panel():
    return render_template('/admin_panel.html')

@app.route('/settings')
@login_required
def settings():
    return render_template('user_settings.html')
    
@app.route('/delete/<product_code>', methods=['GET', 'POST'])
@admin_only
@login_required
def delete_item(product_code):
    if request.method == "POST":
        if product_code.startswith('ACC'):
            item = db.session.execute(db.select(Accessories).filter_by(prod_code=product_code)).scalar_one()
            db.session.delete(item)
            db.session.commit()
            flash("Item deleted")
            return redirect('admin-delete')
        elif product_code.startswith('JXE'):
            item = db.session.execute(db.select(Jeans).filter_by(prod_code=product_code)).scalar_one()
            db.session.delete(item)
            db.session.commit()
            flash("Item deleted")
            return redirect('admin-delete')
        elif product_code.startswith('SHO'):
            item = db.session.execute(db.select(Shoes).filter_by(prod_code=product_code)).scalar_one()
            db.session.delete(item)
            db.session.commit()
            flash("Item deleted")
            return redirect('admin-delete')
        elif product_code.startswith('SHP'):
            item = db.session.execute(db.select(Tshirts).filter_by(prod_code=product_code)).scalar_one()
            db.session.delete(item)
            db.session.commit()
            flash("Item deleted")
            return redirect('admin-delete')
    return redirect('/admin-panel')
# This route is used for deleting stock by admin
@app.route('/admin-delete', methods=['GET', 'POST'])
@admin_only
@login_required
def admin_panel_delete():
    if request.method == 'POST':
        item = request.form.get('item-select')
        if item == 'accessories':
            # Run SQL query to get all accessories
            accessories = Accessories.query.all()   
            print(accessories)
            return render_template('admin_delete.html', item_name=item, query_result=accessories)
        elif item == 'shirts':
            shirt = Tshirts.query.all()
            return render_template('admin_delete.html', item_name=item, query_result=shirt)
        elif item == 'shoes':
            shoes = Tshirts.query.all()
            return render_template('admin_delete.html', item_name=item, query_result=shoes)
        elif item == 'jeans':
            jeans = Jeans.query.all()
            return render_template('admin_delete.html', item_name=item, query_result=jeans)
    return redirect('/')

@app.route('/item-form', methods=['GET', 'POST'])
@admin_only
@login_required
def generate_form():
    if request.method == 'POST':
        item = request.form['item-select']
    return render_template('admin_panel.html', item=item)

@app.route('/accessories-form', methods=['GET', 'POST'])
@admin_only
@login_required
def accessories_form():
    if request.method == 'POST':
        image = request.files['image']
        file_path = upload_file(app, image)
        if not file_path:
            flash("Error with file upload")
            return redirect('/admin-panel')
        name = request.form.get('name')
        qty = request.form.get('qty')
        price = request.form.get('price')
        type = request.form.get('type')
        prod_code = generate_product_code('ACC', 7)
        product = ProductTable(name=name, price=price, prod_code=prod_code
                               ,image_path=file_path)
        db.session.add(product)
        db.session.commit()
        accessory = Accessories(name=name, price=price, qty=qty, type=type, 
                                image_path=file_path, product_table_id=product.id,
                                prod_code=prod_code)
        db.session.add(accessory)
        db.session.commit()
    return render_template('admin_panel.html', item='accessories')

@app.route('/jeans-form', methods=['GET', 'POST'])
@admin_only
@login_required
def jeans_form():
    if request.method == 'POST':
        image = request.files['image']
        file_path = upload_file(app, image)
        if not file_path:
            flash("Error with file upload")
            return redirect('/admin-panel')
        name = request.form.get('name')
        qty = request.form.get('qty')
        price = request.form.get('price')
        type = request.form.get('type')
        gender = request.form.get('gender')
        prod_code = generate_product_code('JXE', 7)
        product = ProductTable(name=name, price=price, prod_code=prod_code,
                               image_path=file_path)
        db.session.add(product)
        db.session.commit()
        product = ProductTable.query.filter_by(name=name).first()
        jeans = Jeans(name=name, price=price, qty=qty, type=type, gender=gender, 
                                image_path=file_path, product_table_id=product.id,
                                prod_code=prod_code)
        db.session.add(jeans)
        db.session.commit()
    return render_template('admin_panel.html', item='jeans')

@app.route('/shoes-form', methods=['GET', 'POST'])
@admin_only
@login_required
def shoes_form():
    if request.method == 'POST':
        image = request.files['image']
        file_path = upload_file(app, image)
        if not file_path:
            flash("Error with file upload")
            return redirect('/admin-panel')
        name = request.form.get('name')
        qty = request.form.get('qty')
        price = request.form.get('price')
        type = request.form.get('type')
        gender = request.form.get('gender')
        prod_code = generate_product_code('SHO', 7)
        product = ProductTable(name=name, price=price,
                               image_path=file_path, prod_code=prod_code)
        db.session.add(product)
        db.session.commit()
        product = ProductTable.query.filter_by(name=name).first()
        shoes = Shoes(name=name, price=price, qty=qty, type=type, gender=gender, 
                                image_path=file_path, product_table_id=product.id,
                                prod_code=prod_code)
        db.session.add(shoes)
        db.session.commit()
    return render_template('admin_panel.html', item='shoes')

@app.route('/shirt-form', methods=['GET', 'POST'])
@admin_only
@login_required
def fill_acc_form():
    if request.method == 'POST':
        image = request.files['image']
        file_path = upload_file(app, image)
        if not file_path:
            flash("Error with file upload")
            return redirect('/admin-panel')
        name = request.form.get('name')
        qty = request.form.get('qty')
        price = request.form.get('price')
        type = request.form.get('type')
        gender = request.form.get('gender')
        prod_code = generate_product_code('SHP', 7)
        product = ProductTable(name=name, price=price, image_path=file_path,
                               prod_code=prod_code)
        db.session.add(product)
        db.session.commit()
        product = ProductTable.query.filter_by(name=name).first()
        shirts = Tshirts(name=name, price=price, qty=qty, type=type, gender=gender, 
                                image_path=file_path, product_table_id=product.id,
                                prod_code=prod_code)
        db.session.add(shirts)
        db.session.commit()
    return render_template('admin_panel.html', item='shirts')

@app.route('/view-item/<item_code>', methods=['GET', 'POST'])
def product_view(item_code):
    if item_code.startswith('ACC'):
        result = db.session.execute(
            db.select(Accessories)
            .where(Accessories.prod_code==item_code)
        )
    elif item_code.startswith('SHP'):
        result = db.session.execute(
            db.select(Tshirts)
            .where(Tshirts.prod_code==item_code)
        )
    elif item_code.startswith('SHO'):
        result = db.session.execute(
            db.select(Shoes)
            .where(Shoes.prod_code==item_code)
        )
    elif item_code.startswith('JXE'):
        result = db.session.execute(
            db.select(Jeans)
            .where(Jeans.prod_code==item_code)
        )
    result_row = []
    for chunk in result:
        for row in chunk:
            result_row.append(row)
    if len(result_row) <= 0:
        return redirect("/")
    return render_template('item_view.html', item=result_row, base_url=request.url_root)

@app.route('/purchase/<item_code>', methods=['POST', 'GET'])
@login_required
def purchase_form(item_code):
    if request.method == 'POST':
        # Query the item that the user want to view
        if item_code.startswith('ACC'):
            result = db.session.execute(
            db.select(Accessories)
            .where(Accessories.prod_code==item_code)
        )
        elif item_code.startswith('SHP'):
            result = db.session.execute(
                db.select(Tshirts)
                .where(Tshirts.prod_code==item_code)
            )
        elif item_code.startswith('SHO'):
            result = db.session.execute(
                db.select(Shoes)
                .where(Shoes.prod_code==item_code)
            )
        elif item_code.startswith('JXE'):
            result = db.session.execute(
            db.select(Jeans)
            .where(Jeans.prod_code==item_code)
        )
            
        item_list = []
        for chunk in result:
            for row in chunk:
                item_list.append(row)
        # Check for button click
        button_click = request.form['form-button']
        if button_click == 'buy-now':
            # Deduct the quanity of the item from the amount the user purchased
            qty_purchased = int(request.form.get('quantity'))
            if qty_purchased > item_list[0].qty or qty_purchased <= 0:
                flash("You cannot order that much!")
                return redirect(f'/view-item/{item_code}')
            print(item_code)
            print("Quantity purchased: ", qty_purchased)
            # Subtract qty from qty in item database
            db.session.execute(
                db.update(Accessories)
                .where(Accessories.prod_code == item_code)
                .values(qty=Accessories.qty - qty_purchased)
            )
            db.session.commit()
            print("Update executed")
            # Add the product as purchased in orders table
            order = Orders(total_price=item_list[0].price * qty_purchased, qty_ordered=qty_purchased ,name=item_list[0].name,
                        users_id=current_user.id, image_path=item_list[0].image_path)
            db.session.add(order)
            db.session.commit()
            print("orders updated")
        elif button_click == 'add-to-cart':
            pass
    return redirect(url_for('orders_page', username=current_user.Name))

from flask import jsonify
# The route used for searching items
@app.route('/search', methods=['POST'])
def search():
    search_query = request.form.get('search_query')
    like_statement = '%{}%'.format(search_query)
    item_name = ProductTable.query.filter(ProductTable.name.like(like_statement)).all()
    result = []
    for item in item_name:
        result.append({
            'name': item.name,
            'price': item.price,
            'product_code': item.prod_code,
            'image_path': item.image_path
        })
    return jsonify(result)
# Once user purchases an item, they can view their oder history from this route
@app.route('/<username>/orders')
@login_required
def orders_page(username):
    user_id = current_user.id
    if username != current_user.Name:
        return redirect(url_for('orders_page', username=current_user.Name))
    print("curr id ", user_id)
    result = (
        db.session.query(Orders)
        .join(Users)
        .filter(Users.id == current_user.id)
        .all()
    )
    result_row = []
    for row in result:
        result_row.append(row)
    return render_template('orders.html', username=username, orders=result_row , base_url=request.url_root)

@app.route('/signup', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        ph_n = request.form.get('phone_number')
        password = request.form.get('password')
        address = request.form.get('address')
        user = Users.query.filter_by(email=email).first()
        if user:
            # If a user with email already exists
            flash("User already exists!")
            return redirect('/signup')
        new_user = Users(email=email, Name=name, Phone_no=ph_n, location=address,
                         password=bcrypt.generate_password_hash(password).decode('utf-8'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Users.query.filter_by(email=email).first()
        if user is None:
            flash('User not found!')
            return redirect('/login')
        if bcrypt.check_password_hash(user.password, password) == False:
            flash("Incorrect Password!")
            return redirect('/login')
        login_user(user=user)
        session['logged_in'] = True
        return redirect('/')
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    if session['logged_in']:
        del session['logged_in']
    flash('Logged out Successfully', 'success')
    return redirect('/')

@app.route('/view-item-<item_name>')
def view_item_subset(item_name):
    if item_name == 'shirts':
        shirt = Tshirts.query.all()
        return render_template('item_filter_view.html', items=shirt, base_url=request.url_root)
    elif item_name == 'shoes':
        shoes = Shoes.query.all()
        return render_template('item_filter_view.html', items=shoes, base_url=request.url_root)
    elif item_name == 'accessories':
        access = Accessories.query.all()
        return render_template('item_filter_view.html', items=access, base_url=request.url_root)
    elif item_name == 'jeans':
        jeans = Jeans.query.all()
        return render_template('item_filter_view.html', items=jeans, base_url=request.url_root)
    return redirect('/')

# Once the app starts initialize the database
# Create tables/database if it is not created
# This also created connection to database file
with app.app_context():
    db.init_app(app)
    db.create_all()
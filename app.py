from flask import Flask, abort, request, render_template, session, flash, redirect,url_for
from flask_login import login_required, logout_user, current_user ,UserMixin, LoginManager, login_user
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from helper import generate_product_code, upload_file
from datetime import datetime
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

class Accessories(db.Model):
    __tablename__ = 'Accessories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(100), nullable=False)
    prod_code = db.Column(db.String(50), nullable=False, unique=True)
    Product_table_id = db.Column(db.Integer, db.ForeignKey('Product_table.id'), nullable=False)
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
    Product_table_id = db.Column(db.Integer, db.ForeignKey('Product_table.id'), nullable=False)
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

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/')
def index():
    accessories = Accessories.query.all()
    shirts = Tshirts.query.all()
    for sh in shirts:
        print(sh.name)
    return render_template('index.html', item_list=[accessories, shirts])

@app.route('/admin-panel')
@login_required
def admin_panel():
    id = current_user.id
    if id == 1:
        return render_template('admin_panel.html')
    else:
        flash("You are not the admin")
        return redirect('/login')

@app.route('/item-form', methods=['GET', 'POST'])
@login_required
def generate_form():
    if current_user.id == 1:
        if request.method == 'POST':
            print(request.form['item-select'])
            item = request.form['item-select']
        return render_template('admin_panel.html', item=item)
    return redirect('/')

@app.route('/accessories-form', methods=['GET', 'POST'])
@login_required
def accessories_form():
    if current_user.id == 1:
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
            product = ProductTable(name=name, price=price)
            db.session.add(product)
            db.session.commit()
            product = ProductTable.query.filter_by(name=name).first()
            accessory = Accessories(name=name, price=price, qty=qty, type=type, 
                                    image_path=file_path, Product_table_id=product.id,
                                    prod_code=generate_product_code('ACC', 7))
            db.session.add(accessory)
            db.session.commit()
        return render_template('admin_panel.html', item='accessories')
    return redirect('/')

@app.route('/jeans-form', methods=['GET', 'POST'])
@login_required
def jeans_form():
    if current_user.id == 1:
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
            product = ProductTable(name=name, price=price)
            db.session.add(product)
            db.session.commit()
            product = ProductTable.query.filter_by(name=name).first()
            jeans = Jeans(name=name, price=price, qty=qty, type=type, gender=gender, 
                                    image_path=file_path, Product_table_id=product.id,
                                    prod_code=generate_product_code('JXE', 7))
            db.session.add(jeans)
            db.session.commit()
        return render_template('admin_panel.html', item='jeans')
    return redirect('/')

@app.route('/shoes-form', methods=['GET', 'POST'])
@login_required
def shoes_form():
    if current_user.id == 1:
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
            product = ProductTable(name=name, price=price)
            db.session.add(product)
            db.session.commit()
            product = ProductTable.query.filter_by(name=name).first()
            shoes = Shoes(name=name, price=price, qty=qty, type=type, gender=gender, 
                                    image_path=file_path, Product_table_id=product.id,
                                    prod_code=generate_product_code('SHO', 7))
            db.session.add(shoes)
            db.session.commit()
        return render_template('admin_panel.html', item='shoes')
    return redirect('/')

@app.route('/shirt-form', methods=['GET', 'POST'])
@login_required
def fill_acc_form():
    if current_user.id == 1:
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
            product = ProductTable(name=name, price=price)
            db.session.add(product)
            db.session.commit()
            product = ProductTable.query.filter_by(name=name).first()
            shirts = Tshirts(name=name, price=price, qty=qty, type=type, gender=gender, 
                                    image_path=file_path, Product_table_id=product.id,
                                    prod_code=generate_product_code('SHP', 7))
            db.session.add(shirts)
            db.session.commit()
        return render_template('admin_panel.html', item='shirts')
    return redirect('/')

@app.route('/view-item/<item_code>', methods=['GET', 'POST'])
def product_view(item_code):
    result = db.session.execute(
        db.select(Accessories)
        .where(Accessories.prod_code==item_code)
    )
    result_row = []
    for chunk in result:
        for row in chunk:
            result_row.append(row)
    if len(result_row) <= 0:
        return redirect("/")
    return render_template('item_view.html', item=result_row)

@app.route('/purchase/<item_code>', methods=['POST', 'GET'])
@login_required
def purchase_form(item_code):
    if request.method == 'POST':
        # Query the item that the user want to view
        result = db.session.execute(
            db.select(Accessories)
            .where(Accessories.prod_code==item_code)
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
            order = Orders(total_price=item_list[0].price, qty_ordered=qty_purchased ,name=item_list[0].name,
                        users_id=current_user.id, image_path=item_list[0].image_path)
            db.session.add(order)
            db.session.commit()
            print("orders updated")
        elif button_click == 'add-to-cart':
            pass
    return redirect(url_for('orders_page', username=current_user.Name))

@app.route('/<username>/orders')
@login_required
def orders_page(username):
    user_id = current_user.id
    print("curr id ", user_id)
    # result = db.session.execute(
    #     db.select(Orders)
    #     .filter_by(users_id=user_id)
    # )
    result = db.session.query(
        Orders, Users
    ).filter(
        Orders.users_id == Users.id
    ).all()
    return render_template('orders.html', username=username, orders=result)

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

@app.route('/shirts', methods=['POST', 'GET'])
def shirts():
    if request.method == 'POST':
        pass
    return render_template('shirts.html')

@app.route('/shoes', methods=['POST', 'GET'])
def shoes():
    return render_template('shoes.html')

with app.app_context():
    db.init_app(app)
    db.create_all()
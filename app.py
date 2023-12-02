from flask import Flask, abort, request, render_template, session, flash, redirect,url_for
from flask_login import login_required, logout_user, current_user ,UserMixin, LoginManager, login_user
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'super secret!'
app.config['UPLOAD_FOLDER'] = 'images'
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
    Name = db.Column(db.String(100), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    Qty = db.Column(db.Integer, nullable=False)
    Type = db.Column(db.String(100), nullable=False)
    Product_table_id = db.Column(db.Integer, db.ForeignKey('Product_table.id'), nullable=False)
    product = db.relationship('ProductTable', backref='accessories')
    image_path = db.Column(db.String(255))

class Admin(db.Model, UserMixin):
    __tablename__ = 'Admin'

    id = db.Column(db.Integer, primary_key=True)
    Password = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), nullable=False)

class Jeans(db.Model):
    __tablename__ = 'Jeans'

    Gender = db.Column(db.String(1), nullable=False)
    Type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    Qty = db.Column(db.Integer, nullable=False)
    Product_table_id = db.Column(db.Integer, db.ForeignKey('Product_table.id'), nullable=False)
    product = db.relationship('ProductTable', backref='jeans')
    image_path = db.Column(db.String(255))

class Orders(db.Model):
    __tablename__ = 'Orders'

    id = db.Column(db.Integer, primary_key=True)
    Total_price = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    Users_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    user = db.relationship('Users', backref='orders')
    
class Shoes(db.Model):
    __tablename__ = 'Shoes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    type = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    Qty = db.Column(db.Integer, nullable=False)
    Price = db.Column(db.Integer, nullable=False)
    Product_table_id = db.Column(db.Integer, db.ForeignKey('Product_table.id'), nullable=False)
    product = db.relationship('ProductTable', backref='shoes')
    image_path = db.Column(db.String(255))

class Tshirts(db.Model):
    __tablename__ = 'Tshirts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    Qty = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    Price = db.Column(db.Integer, nullable=False)
    Gender = db.Column(db.String(1), nullable=False)
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

class OrderDetails(db.Model):
    __tablename__ = 'order_details'

    id = db.Column(db.Integer, primary_key=True)
    Qty = db.Column(db.Integer, nullable=False)
    Name = db.Column(db.String(100), nullable=False)
    Total_p = db.Column(db.Integer, nullable=False)
    Orders_id = db.Column(db.Integer, db.ForeignKey('Orders.id'), nullable=False)
    orders = db.relationship('Orders', backref='order_details')
    Product_table_id = db.Column(db.Integer, db.ForeignKey('Product_table.id'), nullable=False)
    product = db.relationship('ProductTable', backref='order_details')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def upload_file(file):
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        return file_path
    else:
        return False

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

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
            file_path = upload_file(image)
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
            accessory = Accessories(Name=name, price=price, Qty=qty, Type=type, 
                                    image_path=file_path, Product_table_id=product.id)
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
            file_path = upload_file(image)
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
            jeans = Jeans(name=name, price=price, Qty=qty, Type=type, Gender=gender, 
                                    image_path=file_path, Product_table_id=product.id)
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
            file_path = upload_file(image)
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
            shoes = Shoes(name=name, Price=price, Qty=qty, type=type, gender=gender, 
                                    image_path=file_path, Product_table_id=product.id)
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
            file_path = upload_file(image)
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
            shirts = Tshirts(name=name, Price=price, Qty=qty, type=type, Gender=gender, 
                                    image_path=file_path, Product_table_id=product.id)
            db.session.add(shirts)
            db.session.commit()
        return render_template('admin_panel.html', item='shirts')
    return redirect('/')
# @app.route('/admin-login', methods=['POST', 'GET'])
# def admin_login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         print(bcrypt.generate_password_hash(password).decode())
#         admin = Admin.query.filter_by(username=username).first()
#         if admin is None:
#             flash("Incorrect Credentials!")
#             return redirect('/login')
#         if bcrypt.check_password_hash(admin.Password,
#                                       password) == False:
#             flash("Incorrect Credentials!")
#             return redirect('login')
#         print(current_user)
#         return redirect('/admin-panel')
#     return render_template('admin_login.html')

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
from flask import Flask, request, render_template, session, flash, redirect
from flask_login import login_required, UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'super secret!'
app.config['UPLOAD_FOLDER'] = '/images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wavy.db'
login_manager = LoginManager(app)
db = SQLAlchemy()
bcrypt = Bcrypt(app)

class ProductTable(db.Model):
    __tablename__ = 'Product_table'

    P_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(255))

class Accessories(db.Model):
    __tablename__ = 'Accessories'

    A_id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    Qty = db.Column(db.Integer, nullable=False)
    Type = db.Column(db.String(100), nullable=False)
    Product_table_P_id = db.Column(db.Integer, db.ForeignKey('Product_table.P_id'), nullable=False)
    product = db.relationship('ProductTable', backref='accessories')

class Admin(db.Model):
    __tablename__ = 'Admin'

    Password = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    A_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Jeans(db.Model):
    __tablename__ = 'Jeans'

    Gender = db.Column(db.String(1), nullable=False)
    Type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    J_id = db.Column(db.Integer, primary_key=True)
    Qty = db.Column(db.Integer, nullable=False)
    Product_table_P_id = db.Column(db.Integer, db.ForeignKey('Product_table.P_id'), nullable=False)
    product = db.relationship('ProductTable', backref='jeans')

class Orders(db.Model):
    __tablename__ = 'Orders'

    O_id = db.Column(db.Integer, primary_key=True)
    Total_price = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    Users_U_id = db.Column(db.Integer, db.ForeignKey('Users.U_id'), nullable=False)
    user = db.relationship('Users', backref='orders')

class Shoes(db.Model):
    __tablename__ = 'Shoes'

    S_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(1), nullable=False)
    Qty = db.Column(db.Integer, nullable=False)
    Price = db.Column(db.Integer, nullable=False)
    Product_table_P_id = db.Column(db.Integer, db.ForeignKey('Product_table.P_id'), nullable=False)
    product = db.relationship('ProductTable', backref='shoes')

class Tshirts(db.Model):
    __tablename__ = 'Tshirts'

    T_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    Price = db.Column(db.Integer, nullable=False)
    Gender = db.Column(db.String(1), nullable=False)
    Product_table_P_id = db.Column(db.Integer, db.ForeignKey('Product_table.P_id'), nullable=False)
    product = db.relationship('ProductTable', backref='tshirts')

class Users(db.Model):
    __tablename__ = 'Users'

    U_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    Phone_no = db.Column(db.Integer, nullable=False)
    Nmae = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(50), nullable=False)

class OrderDetails(db.Model):
    __tablename__ = 'order_details'

    OD_id = db.Column(db.Integer, primary_key=True)
    Qty = db.Column(db.Integer, nullable=False)
    Name = db.Column(db.String(100), nullable=False)
    Total_p = db.Column(db.Integer, nullable=False)
    Orders_O_id = db.Column(db.Integer, db.ForeignKey('Orders.O_id'), nullable=False)
    orders = db.relationship('Orders', backref='order_details')
    Product_table_P_id = db.Column(db.Integer, db.ForeignKey('Product_table.P_id'), nullable=False)
    product = db.relationship('ProductTable', backref='order_details')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Assuming you have a ProductTable instance to associate the image with
        product = ProductTable.query.get(1)  # Replace with your actual product ID
        product.image_path = file_path
        db.session.commit()

        return 'File uploaded successfully'

    else:
        return 'Invalid file type'

@login_manager.user_loader
def load_user(user_id):
    return Users.get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def sign_up():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

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
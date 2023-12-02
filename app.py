from flask import Flask, request, render_template, session
from flask_login import login_required, UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'super secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wavy.db'
login_manager = LoginManager(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(UserMixin, db.Model):
    """
    user table, customers
    """
    pass

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shirts', methods=['POST', 'GET'])
def shirts():
    if request.method == 'POST':
        pass
    return render_template('shirts.html')

with app.app_context():
    db.create_all()
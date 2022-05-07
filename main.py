from flask import Flask, redirect, render_template, url_for
from flask_login import LoginManager, login_user, logout_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
load_dotenv()
from models.forms import LoginForm, RegisterForm, PostsForm


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
bd_config = os.getenv('JAWSDB_MARIA_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = bd_config
login_manager = LoginManager(app)
db = SQLAlchemy(app)

@login_manager.user_loader
def get_user(user_id):
    return User.query.filter_by(id=user_id).first()



class User(db.Model, UserMixin):
    __tablename__ = 'tb_users'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255),nullable=False, unique=True )
    cpf = db.Column(db.String(255),nullable=False, unique=True )
    cep = db.Column(db.String(255),nullable=False )
    password = db.Column(db.String(255),nullable=False)
    choice = db.Column(db.String(255),nullable=False)
    sex = db.Column(db.String(255), nullable=False)

    def __init__(self, username, email, cpf, cep, password, choice, sex):
        self.username = username
        self.email = email
        self.cpf = cpf
        self.cep = cep
        self.password = generate_password_hash(password)
        self.choice = choice
        self.sex = sex

    def verify_password(self, password):
        return check_password_hash(self.password, password)
        

class Posts(db.Model):
    __tablename__ = 'tb_posts'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)

    def __init__(self, title, description, author):
        self.title = title
        self.description = description
        self.author = author

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/Discovery')
def discovery():
    posts = Posts.query.all()
    return render_template('discovery.html', posts = posts)


@app.route('/Logged', methods=["GET", "POST"])
def logged():
    msg = ''
    form = PostsForm()
    if form.validate_on_submit():
        title = form.title.data
        author = form.author.data
        description = form.description.data
        post = Posts(title, description, author)
        db.session.add(post)
        db.session.commit()
        msg = 'Post cadastrado com sucesso!'
    return render_template('logged.html',form = form, msg = msg)


@app.route('/Login', methods=["GET", "POST"])
def login():
    msg =''
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email = email).first()
        if not user or not user.verify_password(password):
            msg = 'Email or Password invalid'
        else:
            login_user(user)
            return redirect(url_for('logged'))#tudo em minúscu pq sim
    return render_template('login.html', form = form, msg = msg)

@app.route('/Logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/Register', methods=["GET", "POST"])
def register():
    msg = ''
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        c_email = form.conf_email.data 
        password = form.password.data
        c_pass = form.conf_pass.data
        cep = form.cep.data
        cpf = form.cpf.data
        sex = form.sex.data
        choice = form.select.data

        if email == c_email and password==c_pass:
            user = User(username, email, cpf, cep, password, choice, sex)
            db.session.add(user)
            db.session.commit()
            msg = 'Account Created'

        else:
            msg = 'Email or Password invalid'
    
    return render_template('register.html', form =  form, msg = msg)


if __name__ == '__main__':
    app.run(debug=True)
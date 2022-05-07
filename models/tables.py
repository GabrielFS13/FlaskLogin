from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from main import db, login_manager
from flask_login import UserMixin


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
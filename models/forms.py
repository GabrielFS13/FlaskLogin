from ast import Pass
from tokenize import String
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SelectField, RadioField, TextAreaField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired()])
    password =  PasswordField('password', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    conf_email = EmailField('conf_email', validators=[DataRequired()])
    cpf = StringField('cpf', validators=[DataRequired()])
    cep = StringField('cep', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    conf_pass = PasswordField('conf_pass', validators=[DataRequired()])
    select = SelectField(u'Programming Language', choices=[('Select a language'),('C#'),('PHP'),('Python'),('Java'),('HTML')])
    sex = RadioField('sex', choices=[('Male'), ('Female'), ('Other')])


class PostsForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    author = StringField('author', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])


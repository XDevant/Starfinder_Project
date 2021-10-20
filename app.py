from flask import Flask, render_template, request, flash, redirect,url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'oups'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///starfinder.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login = LoginManager(app)
login.login_view = 'login'

import routes
from models import User

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
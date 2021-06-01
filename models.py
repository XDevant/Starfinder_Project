from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType
import pickle


class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(60), index=True, unique=True)
  email = db.Column(db.String(80), index=True, unique=True)
  password_hash = db.Column(db.String(128))
  characters = db.relationship('Character', backref='user', lazy='dynamic')

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
        return check_password_hash(self.password_hash, password) 

  def __repr__(self):
        return '<User {}>'.format(self.username) 

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    strain = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    backgrounf = db.Column(db.String(20))
    class1 = db.Column(db.String(20))
    level1 = db.Column(db.Integer)
    class2 = db.Column(db.String(20))
    level2 = db.Column(db.Integer)
    skill_ranks = db.Column(MutableList.as_mutable(PickleType), default=[])
    player = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<PC: {}>'.format(self.description)

class Pclass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    hp = db.Column(db.Integer)
    sp = db.Column(db.Integer)
    key_ability = db.Column(db.Integer)
    gbab = db.Column(db.Boolean)
    gfort = db.Column(db.Boolean)
    gref = db.Column(db.Boolean)
    gwill = db.Column(db.Boolean)
    armor_prof = db.Column(MutableList.as_mutable(PickleType))
    wp_prof = db.Column(MutableList.as_mutable(PickleType))
    c_skills = db.Column(MutableList.as_mutable(PickleType))





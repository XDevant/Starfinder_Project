from flask import request, render_template, flash, redirect,url_for
from models import User, Character
from forms import RegistrationForm,LoginForm, CharacterForm
from werkzeug.urls import url_parse
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from app import app, db


@app.route('/')
def index():
  characters = Character.query.all()
  if not characters:
    characters=[]
  return render_template('landing_page.html',characters=characters)


@app.route('/login', methods=['GET', 'POST'])
def login():
  #check if current_user logged in, if so redirect to a page that makes sense
  if current_user.is_authenticated:
        return redirect(url_for('user', username=current_user.username))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user is None or not user.check_password(form.password.data):
      flash('Invalid username or password')
      return redirect(url_for('login'))
    login_user(user, remember=form.remember_me.data)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
      next_page = url_for('user', username=current_user.username)
    return redirect(next_page)
  return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
  #check if current_user logged in, if so redirect to a page that makes sense
    if current_user.is_authenticated:
        return redirect(url_for('user', username=current_user.username))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>',methods=['GET', 'POST'])
@login_required
def user(username):
	user = User.query.filter_by(username=current_user.username).first()
	characters = Character.query.filter_by(player=user.id)
	if characters is None:
		characters = []
	return render_template('user.html', user=user, characters=characters)


@app.route('/user/<username>/character_creation',methods=['GET', 'POST'])
@login_required
def character_creation(username):
  user = User.query.filter_by(username=current_user.username).first()
  form = CharacterForm()
  if request.method == 'POST' and form.validate():
    new_character = Character(name = form.name.data, strain=form.strain.data, class1=form.class1.data, player=current_user.id)
    db.session.add(new_character)
    db.session.commit()
    return render_template('character_selection.html', user=user, charactername=new_character)
  else:
    flash(form.errors)
    return render_template('character_creation.html', user=user, form=form)


@app.route('/user/<username>/<charactername>',methods=['GET', 'POST'])
@login_required
def character_selection(username,charactername):
  user = User.query.filter_by(username=current_user.username).first()
  character = Character.query.filter_by(name=charactername).first()
  return render_template('character_selection.html', user=user, charactername=character)


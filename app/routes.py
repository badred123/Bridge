from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, SignupForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from werkzeug.urls import url_parse

#Index view function
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been posted!')
        return redirect(url_for('index'))
    #Creating mock posts
    posts = [
        {
            'author': {'username': 'Jesse'},
            'body': 'Testing the posts!'
        },
        {
            'author': {'username': 'Maxim'},
            'body': 'Just chillin\''
        }
    ]
	return render_template('index.html', title='Home', form=form, posts=posts)

#Login view function
@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Log in', form=form)

#Logout view function
@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

#Signup view function
@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = SignupForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you have signed up for Bridge!')
		return redirect(url_for('login'))
	return render_template('signup.html', title='Sign Up', form=form)

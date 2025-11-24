from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from itsdangerous import URLSafeTimedSerializer
from models import User
from extensions import db
from forms import RegisterForm, LoginForm

auth = Blueprint('auth', __name__)   


# --------------------------
# REGISTER
# --------------------------
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data.lower(),
            password=generate_password_hash(form.password.data)
        )

        db.session.add(user)
        db.session.commit()

        flash('Account created', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


# --------------------------
# LOGIN
# --------------------------
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)


# --------------------------
# LOGOUT
# --------------------------
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))




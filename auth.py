from flask import Blueprint, render_template, redirect, url_for, flash
from models import LoginForm, RegistrationForm, User
from flask_login import login_user, logout_user, login_required
from __init__ import db
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('views.get_all_tasks'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template("login-form.html", form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash('Username already exists. Please choose a different one.', 'danger')
        elif password != confirm_password:
            flash('Passwords do not match.', 'danger')
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

            new_user = User(username=username, password=hashed_password)

            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('auth.login'))

    return render_template("register-form.html", form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

from flask import Blueprint, render_template, redirect, url_for, flash
from models import LoginForm, RegistrationForm
from __init__ import db

auth = Blueprint("auth", __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Implement authentication logic here
        username = form.username.data
        password = form.password.data

        # Example authentication logic (replace with actual logic)
        if username == 'admin' and password == 'password':  # This is just a placeholder
            flash('Login successful!', 'success')
            return redirect(url_for('views.get_all_tasks'))  # Redirect to another page after successful login
        else:
            flash('Invalid username or password.', 'danger')

    return render_template("login-form.html", form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Here you would add logic to save the new user to the database
        # Example: create a new user instance and add to the db
        username = form.username.data
        password = form.password.data

        # Placeholder logic for user registration (replace with actual logic)
        # Check if the username already exists
        if False:  # Replace this with your logic to check if username exists
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            # Example: user = User(username=username, password=hashed_password)
            # db.session.add(user)
            # db.session.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('auth.login'))

    return render_template("register-form.html", form=form)

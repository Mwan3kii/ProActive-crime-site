"""Import necessary modules and functions from Flask and other packages"""
from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Create a Blueprint for authentication routes
auth = Blueprint("auth", __name__)


# Route for logging in users
@auth.route("/login", methods=['GET', 'POST'])
def login():
    # Handle the login process for users.
    if request.method == 'POST': # Validate user credentials and log them in if valid
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first() # Query the user by email
        if user:
            if check_password_hash(user.password, password): # Check if password is correct
                flash("Logged in!", category='success')
                login_user(user, remember=True) # Log the user in
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


# Route for signing up new users
@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    # Handle the sign-up process for new users.
    if request.method == 'POST': # Validate user input and create a new user if valid
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists = User.query.filter_by(email=email).first() # Check if email is already in use
        username_exists = User.query.filter_by(username=username).first() # Check if username is already in use

        # Validate user input
        if email_exists:
            flash('Email is already in use.', category='error')
        elif username_exists:
            flash('Username is already in use.', category='error')
        elif password1 != password2:
            flash('Password don\'t match!', category='error')
        elif len(username) < 2:
            flash('Username is too short.', category='error')
        elif len(password1) < 6:
            flash('Password is too short.', category='error')
        elif len(email) < 4:
            flash("Email is invalid.", category='error')
        else:
            # Create a new user and add to the database
            new_user = User(email=email, username=username, password=generate_password_hash(
                password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True) # Log the new user in
            flash('User created!')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)


# Route for logging out users
@auth.route("/logout")
@login_required
def logout():
    # Log out the current user and redirect to the home page.
    logout_user()
    return redirect(url_for("views.home"))
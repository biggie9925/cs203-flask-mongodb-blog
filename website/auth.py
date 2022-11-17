from flask_login import login_required, current_user, logout_user, login_user
from flask import render_template, redirect, url_for, request, flash, Blueprint
from . import users, posts
import bcrypt
from . models import User
from bson.objectid import ObjectId


auth = Blueprint("auth", __name__)



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        email_found = users.find_one({"email": email})
        if email_found:
            password_val = email_found['password']

            if bcrypt.checkpw(password.encode('utf-8'), password_val):
                loguser = User(
                    email_found["username"], email_found["email"], email_found["password"],
                    email_found['_id'])
                login_user(loguser, remember=True)

                blog_posts = posts.find()

                return render_template('index.html', user=current_user, posts=blog_posts)

            else:
                flash('Wrong Password', category='error')
                return redirect(url_for('auth.login'))
        else:
            flash('Email not found', category='error')
            return redirect(url_for('auth.login'))

    return render_template("login.html", user=current_user)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        existing_username = users.find_one(
            {'username': request.form['username']})
        existing_email = users.find_one({'email': request.form['email']})

        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        if existing_username:
            flash('Username already exists', category="error")
            redirect(url_for('auth.register'))

        elif existing_email:
            flash('Email already exists', category="error")
            redirect(url_for('auth.register'))

        elif len(username) < 2:
            flash("Username is too short", category="error")
            redirect(url_for('auth.register'))
        elif len(password) < 6:
            flash("Password is too short", category="error")
            redirect(url_for('auth.register'))
        elif len(email) < 4:
            flash("Email is invalid", category="error")
            redirect(url_for('auth.register'))


        else:
            hashpass = bcrypt.hashpw(
                request.form['password'].encode('utf-8'), bcrypt.gensalt())

            user_input = {
                'username': request.form['username'], 'email': request.form['email'], 'password': hashpass}

            users.insert_one(user_input)
            flash('User successfully created! Please login', category="success")

            return redirect(url_for('auth.login'))

    return render_template("register.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('auth.login')

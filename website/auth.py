from flask import render_template, redirect, url_for, request, flash, Blueprint, session
from werkzeug.security import generate_password_hash, check_password_hash
from . import db 

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        users = db.users
        user = users.find_one({"username":username})

        if user:
            if check_password_hash(user['password'], password):
                flash("Logged in", category="success")
                return redirect(url_for("views.index"))
            else:
                flash("Password is incorrect", category="error")
        else:
            flash("Email does not exist", category="error")
    return render_template("login.html")


@auth.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        users = db.users

        email_exists = users.count_documents({"email":email})
        username_exists = users.count_documents({"username":username})

        if email_exists == 1:
            flash("Email is already in use", category="error")
        elif username_exists == 1:
            flash("Username is already in use", category="error")
        elif len(username) < 2:
            flash("Username is too short", category="error")
        elif len(password) < 6:
            flash("Password is too short", category="error")
        elif len(email) < 4:
            flash("Email is invalid", category="error")
        else:

            password=generate_password_hash(password, method="sha256")

            new_user = {
                "email": email,
                "username": username,
                "password": password
            }

            users.insert_one(new_user)
            flash("User Created!")
            return redirect(url_for("views.index"))

    return render_template("register.html")

@auth.route('/logout')
def logout():
    if "email" in session:
        session.pop("email", None)
        return redirect(url_for("views.index"))
    else:
        return redirect(url_for("views.index"))
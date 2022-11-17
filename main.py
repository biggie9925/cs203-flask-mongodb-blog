from flask import Flask, render_template, request, url_for, redirect, flash
from flask_login import login_required, current_user, LoginManager, logout_user, login_user
import pymongo
from pymongo import MongoClient
import certifi
from models import User, Post, Enquiry
import bcrypt
from bson.objectid import ObjectId
from bson import json_util


app = Flask(__name__)
app.config['SECRET_KEY'] = "testing"
connection_string = "mongodb+srv://admin:admin123@database.lrh5cyk.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string, tlsCAFile=certifi.where())
db = client.get_database('test')
users = db.test
posts = db.post
enquiries = db.enquiry

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(_id):
    user = users.find_one({'_id': ObjectId(_id)})
    if not user:
        return None
    return User(user['username'], user['email'], user['password'], str(user['_id']))


@app.route('/login', methods=['GET', 'POST'])
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
                # user_obj=User(json_util.dumps(email_found['_id']))
                loguser = User(
                    email_found["username"], email_found["email"], email_found["password"],
                    email_found['_id'])
                login_user(loguser, remember=True)

                blog_posts = posts.find()

                return render_template('index.html', user=current_user, posts=blog_posts)

            else:
                flash('Wrong Password', category='error')
                return redirect(url_for('login'))
        else:
            flash('Email not found', category='error')
            return redirect(url_for('login'))

    return render_template("login.html", user=current_user)


@ app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        existing_username = users.find_one(
            {'username': request.form['username']})
        existing_email = users.find_one({'email': request.form['email']})

        if existing_username:
            flash('Username already exists', category="error")
            redirect(url_for('register'))

        elif existing_email:
            flash('Email already exists', category="error")
            redirect(url_for('register'))

        else:
            hashpass = bcrypt.hashpw(
                request.form['password'].encode('utf-8'), bcrypt.gensalt())

            user_input = {
                'username': request.form['username'], 'email': request.form['email'], 'password': hashpass}

            users.insert_one(user_input)
            flash('User successfully created! Please login', category="success")

            return redirect(url_for('login'))

    return render_template("register.html", user=current_user)


@ app.route("/logout")
@ login_required
def logout():
    logout_user()
    return redirect('login')


@ app.route('/', methods=['GET', 'POST'])
@ app.route('/home', methods=['GET', 'POST'])
def index():
    blog_posts = posts.find()

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        if not name or not email or not phone or not message:
            flash('All fields required', category="error")
            return redirect(url_for('index'))
        else:
            enquiry = Enquiry(name, email, phone, message)
            enquiries.insert_one(enquiry.json())
            flash('Enquiry Received', category="success")
            return redirect(url_for('index'))

    return render_template("index.html", user=current_user, posts=blog_posts)


@ app.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        imgURL = request.form.get('imgURL')

        if not title:
            flash('Title cannot be empty', category="error")
            return redirect(url_for('write'))
        if not content:
            flash('Post cannot be empty', category="error")
            return redirect(url_for('write'))
        else:
            new_post = Post(current_user.username, title, content, imgURL)
            posts.insert_one(new_post.json())
            flash('Post Created', category="success")
            return redirect(url_for('index'))
    return render_template("write.html", user=current_user)


@ app.route('/posts/<string:post_id>')
def single_post(post_id):
    single_post = posts.find_one({'_id': post_id})
    return render_template("single_post.html", user=current_user, post=single_post)


@ app.route('/delete/<string:post_id>')
def delete(post_id):
    delete_post = posts.find_one({'_id': post_id})
    if not current_user.is_authenticated:
        flash("You do not have permission to delete this post", category="error")
        return redirect(url_for('single_post', post_id=post_id))
    elif current_user.username != delete_post['username'][0]:
        flash("You do not have permission to delete this post", category="error")
        return redirect(url_for('single_post', post_id=post_id))
    else:
        posts.delete_one(delete_post)
        flash('Post Deleted', category="success")
    return redirect(url_for('index'))


@ app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "GET":
        return redirect(url_for('index'))
    else:
        posts.create_index([('title', 'text')])
        search = request.form.get('search')
        results = posts.find({"$text": {"$search": search}})
        count = posts.count_documents({"$text": {"$search": search}})

        if count != 0:
            return render_template('index.html', posts=results, user=current_user)
        else:
            message = "Not Found"
            return render_template('index.html', message=message, user=current_user)


if __name__ == '__main__':
    app.run(debug=True)

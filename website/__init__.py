from flask import Flask
import os
from flask_login import LoginManager
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
import certifi
from .models import User
from bson.objectid import ObjectId

load_dotenv(find_dotenv())
password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb+srv://admin:{password}@database.lrh5cyk.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string, tlsCAFile=certifi.where())
db = client.get_database('test')
users = db.test
posts = db.post
enquiries = db.enquiry

def create_app():
    app = Flask(__name__)
    app.secret_key = "helloworld"

    from .views import views
    from .auth import auth

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(_id):
        user = users.find_one({'_id': ObjectId(_id)})
        if not user:
            return None
        return User(user['username'], user['email'], user['password'], str(user['_id']))

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return app
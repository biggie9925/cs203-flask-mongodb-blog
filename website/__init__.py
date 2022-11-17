from flask import Flask
import os
from flask_login import LoginManager
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient

 #database
load_dotenv(find_dotenv())
password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb+srv://david:{password}@cluster0.asfrwam.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)
db = client.cs203

def create_app():
    app = Flask(__name__)
    app.secret_key = "helloworld"

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return app
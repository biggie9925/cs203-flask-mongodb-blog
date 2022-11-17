from datetime import datetime
import uuid


# User class
class User():
    def __init__(self, username, email, password, _id=None):
        # Main initialiser
        self.username = username
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "_id": self._id,
            "username": self.username,
            "email": self.email,
            "password": self.password
        }

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self._id)


class Post():
    def __init__(self, username, title, content, imgURL, created_date=datetime.utcnow().strftime("%d %B %Y %H:%M:%S"), _id=None):
        self.username = username,
        self.title = title
        self.content = content
        self.imgURL = imgURL
        self.created_date = created_date
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            '_id': self._id,
            'username': self.username,
            'title': self.title,
            'content': self.content,
            'imgURL': self.imgURL,
            'created_date': self.created_date
        }


class Enquiry():
    def __init__(self,  name, email, phone, message, created_date=datetime.utcnow().strftime("%d %B %Y %H:%M:%S"), _id=None):
        self.name = name
        self.email = email
        self.phone = phone
        self.message = message
        self.created_date = created_date
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            '_id': self._id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'message': self.message,
            'created_date': self.created_date
        }

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/write')
def write():
    return render_template("write.html")


@app.route('/single')
def singe_post():
    return render_template("single_post.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/register')
def register():
    return render_template("register.html")


if __name__ == '__main__':
    app.run(debug=True)

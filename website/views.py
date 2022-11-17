from flask import Flask, render_template, redirect, url_for, request, flash, Blueprint
from . import db

views = Blueprint("views", __name__)

#flask routes
@views.route('/')
@views.route('/home')
def index():
    return render_template("index.html")


@views.route('/write', methods=["GET", "POST"])
def write():
    if request.method == "POST":
        title = request.form.get("title")
        story = request.form.get("story")

        if title == "":
            flash("Please enter a title", category="error")
        elif story == "":
            flash("Please enter your story", category="error")
        else:

            story = {
                "title": title,
                "story": story,
            }

            stories = db.stories
            stories.insert_one(story)
            flash("Story successfully uploaded!", category="success")

        return redirect(url_for("views.write"))

    return render_template("write.html")
    

@views.route('/single')
def single_post():
    return render_template("single_post.html")


@views.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        number = request.form.get("phone")
        message = request.form.get("message")

        if name == "":
            flash("Please enter your name", category="error")
        elif email == "":
            flash("Please enter your email", category="error")
        elif number == "":
            flash("Please enter your contact number", category="error")
        elif message == "":
            flash("Please enter a message", category="error")
        else:

            enquiry = {
                "name": name,
                "email": email,
                "number": number,
                "message": message
            }

            messages = db.messages
            messages.insert_one(enquiry)
            flash("Message sent!", category="success")

        return redirect(url_for("views.index"))







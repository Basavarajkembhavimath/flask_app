from flask import Flask, Blueprint, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db, User, Feedback 
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

web = Blueprint("web", __name__)

# Decorator to protect routes
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("web.register", next=request.path))
        return f(*args, **kwargs)
    return decorated_function


# Home page
@web.route("/")
def home():
    
    return render_template("index.html", username=session.get("username"))

# User Home page
@web.route("/user/<name>")
def user(name):
    return render_template("index.html", username= name)

@web.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already taken!"
        
        # Create new user
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("web.login"))
    return render_template("register.html")



# @web.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]

#         # Check if user already exists
#         existing_user = User.query.filter_by(username=username).first()
#         if existing_user:
#             if request.args.get("format") == "json":
#                 return jsonify({"error": "Username already taken"}), 400
#             return "Username already taken!"

#         # Create new user
#         new_user = User(username=username)
#         new_user.set_password(password)
#         db.session.add(new_user)
#         db.session.commit()

#         if request.args.get("format") == "json":
#             return jsonify({"message": "User registered successfully"}), 201
#         return redirect(url_for("web.login"))

#     # GET request
#     if request.args.get("format") == "json":
#         return jsonify({"info": "Send POST request with username and password"})
#     return render_template("register.html")

# Login page
@web.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Add your authentication login here
        # Look up user in db
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session.permanent = False # ensures session dies when browser closes
            session["logged_in"] = True # Mark user as logged in
            session["username"] = user.username 
            # Redirect to originally requested page is available
            #next_url = session.pop("next_url", None)
            next_url = request.form.get("next") or request.args.get("next")
            # if session.get("logged_in"):
            #     next_url =  request.args.get("next")
            if next_url:
            #     return redirect(next_url or url_for("web.home"), code=303)
            # return redirect(url_for("web.home"), code=303)
                return render_template("login.html", next=request.args.get("next"))
            return render_template("login.html", next=request.args.get("next"))
        else:
            return "Invalid credentials, try again!"

    return render_template("login.html", next=request.args.get("next"))

# Logout
@web.route("/logout")
def logout():
    session.pop("logged_in", None)
    session.clear()
    return redirect(url_for("web.home"))


@web.route("/about")
def about():
    return render_template("about.html")

@web.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        # Save to database
        feedback = Feedback(name=name, email=email, message=message)
        db.session.add(feedback)
        db.session.commit()

        return render_template("thank_you.html")
    return render_template("contact.html")

@web.route("/feedbacks")
def feedbacks():
    all_feedback = Feedback.query.all()
    return render_template("feedbacks.html", feedbacks= all_feedback)


import requests

@web.route("/feedbacks_html")
def feedbacks_html():
    response = requests.get("http://127.0.0.1:5000/api/feedbacks")
    feedbacks = response.json()
    return render_template("feedbacks.html", feedbacks=feedbacks)


@web.route("/api/feedbacks", methods=["GET"])
def api_get_feedbacks():
    all_feedback = Feedback.query.all()
    feedback_list = [
        {"id": f.id, "name": f.name, "email": f.email, "message": f.message}
        for f in all_feedback
    ]
    return jsonify(feedback_list)

# Protected routes
@web.route("/projects")
@login_required
def projects():
    return render_template("projects.html")

@web.route("/resume")
@login_required
def resume():
    return render_template("resume.html")

@web.route("/blog")
@login_required
def blog():
    posts = [
        {"title": "My First Blog Post", "content":"This is a demo post."},
        {"title": "Learning Flask", "content":"Flask makes web webs easy!"}
    ]
    return render_template("blog.html", posts=posts)

# if __name__ == "__main__":
#     #Create tables iside app context
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)
    
    
from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, User, Feedback
from functools import wraps

web = Blueprint("web", __name__)

# Decorator for login protection
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("web.login", next=request.path))
        return f(*args, **kwargs)
    return decorated_function

@web.route("/", endpoint="home")
def home():
    return render_template("index.html", username=session.get("username"))

@web.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Example: create user
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("web.login"))
    return render_template("register.html")


@web.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session["logged_in"] = True
            session["username"] = user.username
            return redirect(url_for("web.home"))
        return "Invalid credentials"
    return render_template("login.html")

@web.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("web.home"))

@web.route("/projects")
@login_required
def projects():
    return render_template("projects.html")

@web.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        feedback = Feedback(
            name = request.form["name"],
            email = request.form["email"],
            message = request.form["message"]
        )
        db.session.add(feedback)
        db.session.commit()
        return render_template("thank_you.html")
    return render_template("contact.html")

@web.route("/about")
def about():
    return render_template("about.html")

@web.route("/blog")
def blog():
    return render_template("blog.html")

@web.route("/resume")
def resume():
    return render_template("resume.html")

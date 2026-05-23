from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from models import db, User, Feedback
# Create db object without passing app
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = "supersecretkey"   # Needed for sessions

    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)


    # Initialize db with app
    db.init_app(app)
    return app

# Define models
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Feedback {self.name} - {self.email}>"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Create app instance
app = create_app()

# Global set to track active users
active_users = set()

# Home page
@app.route("/")
def home():
    next_url = session.pop("next_url", None)
    if next_url:
        return redirect(next_url)
    return render_template("index.html", username=session.get("username"))

@app.route("/admin")
def admin_dashboard():
    # Only allow if current user is 'admin'
    if not session.get("is_admin"):
        return "Access denied"

    # Active users (from global set)
    active = list(active_users)

    # All registered users(from db)
    all_users = User.query.all()
    return render_template(
        "admin.html",
        active_users = active,
        active_count = len(active),
        all_users = all_users,
        total_count = len(all_users) 
        )

    #return render_template("admin.html", users=list(active_users), count=len(active_users))

# Register page
@app.route("/register", methods=["GET", "POST"])
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

        return redirect(url_for("login"))

    return render_template("register.html")

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session.permanent = True
            session["logged_in"] = True
            session["username"] = user.username
            session["is_admin"] = (user.username == "admin") # flag admin

            # Add to active users
            active_users.add(user.username)
            next_url = request.form.get("next") or request.args.get("next")
            if next_url:
                return redirect(next_url)
            return redirect(next_url or url_for("home"), code=303)
        else:
            return "Invalid credentials, try again!"

    return render_template("login.html", next=request.args.get("next"))

# Logout
@app.route("/logout")
def logout():
    if session.get("username") in active_users:
        active_users.remove(session["username"])
    session.pop("logged_in", None)
    session.pop("username", None)
    return redirect(url_for("home"))

# Decorator to protect routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            # Redirect to register first, then login
            return redirect(url_for("login", next=request.path))
        return f(*args, **kwargs)
    return decorated_function

# Protected routes
@app.route("/projects")
@login_required
def projects():
    return render_template("projects.html")

@app.route("/resume")
@login_required
def resume():
    return render_template("resume.html")

@app.route("/blog")
@login_required
def blog():
    posts = [
        {"title": "My First Blog Post", "content": "This is a demo post."},
        {"title": "Learning Flask", "content": "Flask makes web apps easy!"}
    ]
    return render_template("blog.html", posts=posts)

# Other routes
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        feedback = Feedback(name=name, email=email, message=message)
        db.session.add(feedback)
        db.session.commit()

        return render_template("thank_you.html")
    return render_template("contact.html")

@app.route("/feedbacks")
def feedbacks():
    all_feedback = Feedback.query.all()
    return render_template("feedbacks.html", feedbacks=all_feedback)

@app.route("/api/feedbacks", methods=["GET"])
def api_get_feedbacks():
    all_feedback = Feedback.query.all()
    feedback_list = [
        {"id": f.id, "name": f.name, "email": f.email, "message": f.message}
        for f in all_feedback
    ]
    return jsonify(feedback_list)

if __name__ == "__main__":
    with app.app_context():
        if not User.query.filter_by(username="admin").first():
            admin_user = User(username="admin")
            admin_user.set_password("secret") # Choose a strong password
            db.session.add(admin_user)
            db.session.commit()
        db.create_all()
    app.run(debug=True)

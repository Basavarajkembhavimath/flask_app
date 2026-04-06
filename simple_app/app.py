from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create db object without passing app
db = SQLAlchemy()

def create_app():
    
    app = Flask(__name__)

     # Step 2: Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Intialize db with app
    db.init_app(app)

    return app

# Define your model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable= False)
    message = db.Column(db.Text, nullable= False)
    created_at = db.Column(db.DateTime, default=datetime.now) # timestamp

    def __repr__(self):
        return f"<Feedback {self.name} - {self.email}"

# Create app instance
app = create_app()

@app.route("/")
def home():
    
    return render_template("index.html", username="Basavaraj")

@app.route("/user/<name>")
def user(name):
    return render_template("index.html", username= name)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Add your authentication login here
        if username == "admin" and password == "secret":
            return redirect(url_for("index"))
        else:
            return "Invalid credentials, try again!"

    return render_template("login.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
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

@app.route("/feedbacks")
def feedbacks():
    all_feedback = Feedback.query.all()
    return render_template("feedbacks.html", feedbacks= all_feedback)


@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/resume")
def resume():
    return render_template("resume.html")

@app.route("/blog")
def blog():
    posts = [
        {"title": "My First Blog Post", "content":"This is a demo post."},
        {"title": "Learning Flask", "content":"Flask makes web apps easy!"}
    ]
    return render_template("blog.html", posts=posts)

if __name__ == "__main__":
    #Create tables iside app context
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    
    
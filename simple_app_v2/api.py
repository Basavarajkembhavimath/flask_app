from flask import Blueprint, request, jsonify, session
from models import db, User, Feedback

api = Blueprint("api", __name__, url_prefix="/api")

@api.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400
    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@api.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username = data.get("username")).first()
    if user and user.check_password(data.get("password")):
        session["logged_in"] = True
        session["username"] = user.username
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@api.route("/feedbacks", methods=["GET"])
def get_feedbacks():
    feedbacks = Feedback.query.all()
    return jsonify([{"id": f.id, "name": f.name, "email": f.email, "message":f.message} for f in feedbacks])

@api.route("/feedbacks", methods=["POST"])
def add_feedback():
    data = request.get_json()
    feedback = Feedback(name=data["name"], email=data["email"], message=data["message"])
    db.session.add(feedback)
    db.session.commit()
    return jsonify({"message": "Feedback submitted"}), 201


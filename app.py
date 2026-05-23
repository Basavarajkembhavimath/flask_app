from flask import Flask
from models import db
from api import api
from web import web # my existing html routes
from datetime import timedelta


def create_app():
    app = Flask(__name__, template_folder=r"templates")
    app.secret_key = "supersecretkey"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Session expires when browser closes
    app.config["SESSION_PWEMANENT"] = False
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes = 10)

    db.init_app(app)
    app.register_blueprint(api)
    app.register_blueprint(web)

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)


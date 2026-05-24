from flask import Flask
from models import User, db
from api import api
from web import web # my existing html routes
from datetime import timedelta
import os

def create_app():
    #app = Flask(__name__, template_folder=r"templates")
    app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), "templates"))
    app.secret_key = "supersecretkey"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Session expires when browser closes
    app.config["SESSION_PERMANENT"] = False
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes = 10)

    db.init_app(app)
    app.register_blueprint(api)
    app.register_blueprint(web)

    with app.app_context():
        #db.create_all()

         # ✅ Create admin user
        if not User.query.filter_by(username="admin").first():
            admin_user = User(username="admin")
            admin_user.set_password("secret")  # replace with strong password or env var
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created successfully!")

    return app

if __name__ == "__main__":
    app = create_app()
    #app.run(debug=True)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)


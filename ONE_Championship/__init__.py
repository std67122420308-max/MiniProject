import os
from flask import Flask
from .extensions import db, login_manager, bcrypt
from .one_championship.routes import fighter_bp
from .users.routes import users_bp

def create_app():

    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "secretkey")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL",
        "sqlite:///database.db"
    )

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "users.login"

    app.register_blueprint(fighter_bp)
    app.register_blueprint(users_bp, url_prefix="/users")

    return app
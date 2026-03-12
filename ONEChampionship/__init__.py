import os
from flask import Flask
from onechampionship.extensions import db, login_manager, bcrypt
from onechampionship.models import User, Team, ONEChampionship
from onechampionship.core.routes import core_bp
from onechampionship.users.routes import users_bp
from onechampionship.onechampionship.routes import onechampionship_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'users.login'
    login_manager.login_message = 'Please login before access this page!'
    login_manager.login_message_category = 'warning'

    app.register_blueprint(core_bp, url_prefix='/')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(onechampionship_bp, url_prefix='/onechampionships')

    return app
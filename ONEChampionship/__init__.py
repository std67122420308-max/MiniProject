import os
from flask import Flask
from ONEChampionship.extensions import db, login_manager, bcrypt
from ONEChampionship.core.routes import core_bp
from ONEChampionship.users.routes import users_bp
from ONEChampionship.ONEChampionship.routes import ONEChampionship_bp

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'devkey')

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'users.login'
    login_manager.login_message = 'Please login before access this page!'
    login_manager.login_message_category = 'warning'

    app.register_blueprint(core_bp, url_prefix='/')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(ONEChampionship_bp, url_prefix='/ONEChampionships')

    return app
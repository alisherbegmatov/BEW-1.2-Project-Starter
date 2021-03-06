from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)
db = SQLAlchemy(app)
app.static_folder = "static"

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


bcrypt = Bcrypt(app)

from app.auth.routes import auth as auth_routes
from app.main.routes import main as main_routes

app.register_blueprint(main_routes)
app.register_blueprint(auth_routes)

with app.app_context():
    db.create_all()

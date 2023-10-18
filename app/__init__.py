from flask import Flask
from config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user, login_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config.from_object(Config)
login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)
from app import routes, models



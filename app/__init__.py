from flask import Flask
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
login = LoginManager(app)
app.config.from_object(Config)
login.login_view = 'login'
from app import routes

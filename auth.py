"""
File: auth.py
Author: Justin Wittenmeier
Description: Main file for server management tool.

Last Modified: January 1, 2024

"""

from flask import Flask
from flask_login import UserMixin, LoginManager
import config
import secrets

# Creating a user to pass into the login function.
class User(UserMixin):
    def __init__(self, user="admin", password=config.PASSWORD) -> None:
        self.id = user
        self.password = password

# Creating a user object to pass into the login function.
user = User()

# Checking if credentials are correct
def authenticate(password):
    return password == config.PASSWORD

app = Flask(__name__, template_folder='templates', static_folder='static')

app.secret_key = secrets.token_hex(16) if not config.SECRET_KEY else config.SECRET_KEY

authentication = LoginManager()
authentication.init_app(app)

@authentication.user_loader
def load_user(user_id):
    return User(user_id)
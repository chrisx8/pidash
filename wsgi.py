import secrets
import string

from flask import Flask
from flask_wtf.csrf import CSRFProtect


# create a random SECRET KEY
def create_secret_key(length):
    key = ""
    characters = string.ascii_letters + string.digits + string.punctuation
    for i in range(length):
        key += secrets.choice(characters)
    return key


# Create app and load secret key
app = Flask(__name__)
app.config["SECRET_KEY"] = create_secret_key(64)

# initialize csrf protection
csrf = CSRFProtect()
csrf.init_app(app)

# import all views
import views  # noqa F401

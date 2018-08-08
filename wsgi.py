from flask import Flask, send_from_directory
from flask_wtf.csrf import CSRFProtect
from config import SECRET_KEY
import os


# SECRET KEY must be a nonempty string, and (hopefully) over 20 characters long
def check_secret_key():
    if not isinstance(SECRET_KEY, str):
        raise TypeError("'SECRET_KEY' must be a string!")
    elif SECRET_KEY == "":
        raise ValueError("'SECRET_KEY' is empty!")
    elif len(SECRET_KEY) < 20:
        print("WARNING: SECRET_KEY is too short! Make it at least 20 characters long!")


# Create app and load secret key
app = Flask(__name__)
check_secret_key()
app.config['SECRET_KEY'] = SECRET_KEY

# initialize csrf protection
csrf = CSRFProtect()
csrf.init_app(app)

# import all views
import views


# serve static files
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# Indicate that the files in this folder are part of a python package
# Also initialize the extensions here
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler
import os


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"

# This will be used for logging errrors to a file
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # Write a log file called dyscors.log and store it in a folder named logs
    # Also make sure that the log file does not get too big
    file_handler = RotatingFileHandler('logs/dyscors.log', maxBytes=10240,
                                       backupCount=10)

    # Format the log messages in a format that collect a lot of info
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Dyscors startup')


from app import routes, models, errors

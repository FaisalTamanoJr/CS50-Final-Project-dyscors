# Indicate that the files in this folder are part of a python package
# Also initialize the extensions here
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
import logging
from logging.handlers import RotatingFileHandler
import os

# Extension instances
db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
login = LoginManager()
login.login_view = "auth.login"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    login.init_app(app)

    # This will be used for logging errrors to a file
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')

        # Write a log file called dyscors.log and store
        # it in a folder named logs.
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

    # These are blueprints so that the application is not a global variable
    from app.errors import bp as errors_bp
    from app.auth import bp as auth_bp
    from app.main import bp as main_bp
    from app import models
    app.register_blueprint(errors_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)

    return app

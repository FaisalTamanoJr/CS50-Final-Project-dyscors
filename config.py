import os

# the location of the main directory
basedir = os.path.abspath(os.path.dirname(__file__))


# This is where the configuration variables are stored
class Config(object):
    # Get the secret key from an environmental variable or use the fallback
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sv_cheats 1'

    # Get the location of the database or use the app.db in the main directory
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    # Do not send signal to the app whenever there is a change in the database
    SQLALCHEMY_TRACK_MODIFICATIONS = False

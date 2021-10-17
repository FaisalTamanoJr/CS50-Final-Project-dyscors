import os


# This is where the configuration variables are stored
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sv_cheats 1'

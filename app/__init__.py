# This module is use to indicate that the files in this folder are part of a python package
from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import routes

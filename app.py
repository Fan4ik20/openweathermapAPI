"""Module with app settings."""

from flask import Flask

app = Flask(__name__)

db_name = 'weather.db'

from flask import Flask
from .env import KEY
# import os

app = Flask(__name__)
# app.secret_key = os.environ['KEY']
app.secret_key = KEY
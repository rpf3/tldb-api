from flask import Flask

from tldb.api import blueprint
from tldb.database import setup as database

app = Flask(__name__)

app.register_blueprint(blueprint)

database.create()

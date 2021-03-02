from flask import Flask

from tldb.api import blueprint

app = Flask(__name__)

app.register_blueprint(blueprint)

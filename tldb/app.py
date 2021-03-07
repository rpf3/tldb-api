from flask import Flask
from flask_cors import CORS

from tldb.api import blueprint

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})

app.register_blueprint(blueprint)

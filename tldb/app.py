from flask import Flask
from flask_cors import CORS
from flask_smorest import Api

from tldb.api import artists, imports, tracklists, tracks

app = Flask(__name__)
app.config["API_TITLE"] = "tldb"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/"
app.config[
    "OPENAPI_SWAGGER_UI_URL"
] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.25.x/"

api = Api(app)

CORS(app, resources={r"/*": {"origins": "*"}})

api.register_blueprint(artists.blp)
api.register_blueprint(tracks.blp)
api.register_blueprint(tracklists.blp)
api.register_blueprint(imports.blp)

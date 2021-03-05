from flask import Blueprint
from flask_restx import Api

from tldb.api import artists, tracklists, tracks

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)

api.add_namespace(artists.api)
api.add_namespace(tracks.api)
api.add_namespace(tracklists.api)

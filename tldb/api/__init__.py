from flask import Blueprint
from flask_restx import Api

from tldb.api import artist, track, tracklist

blueprint = Blueprint("api", __name__)
api = Api(blueprint)

api.add_namespace(artist.api)
api.add_namespace(track.api)
api.add_namespace(tracklist.api)

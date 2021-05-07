from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint

from tldb import database, models
from tldb.api import utils

blp = Blueprint("tracks", "tracks", url_prefix="/tracks")


@blp.route("")
class Tracks(MethodView):
    def __init__(self):
        self.table = database.TrackTable()

    @blp.response(200, models.TrackSchema(many=True))
    def get(self):
        """
        List all tracks
        """
        params = utils.parse_search_args(request)

        database_response = self.table.search(query=None, params=params)

        return database_response

    @blp.arguments(models.TrackWriteSchema)
    @blp.response(200, models.TrackSchema)
    def post(self, track):
        """
        Create a new track
        """
        tracks = [track]
        database_response = self.table.insert(tracks)

        return database_response[0]

    @blp.arguments(models.TrackSchema(many=True))
    @blp.response(200, models.TrackSchema(many=True))
    def patch(self, tracks):
        """
        Create or update a set of tracks
        """
        database_response = self.table.upsert(tracks)

        return database_response


@blp.route("/<string:id>")
class TracksById(MethodView):
    def __init__(self):
        self.table = database.TrackTable()

    @blp.response(200, models.TrackSchema)
    def get(self, id):
        """
        Get a single track
        """
        verbose = request.args.get("verbose") == "1"

        ids = [id]

        database_response = self.table.get(ids, verbose=verbose)

        return database_response[0]

    @blp.arguments(models.TrackWriteSchema)
    @blp.response(200, models.TrackSchema)
    def put(self, track, id):
        """
        Update a single track
        """
        track.id = id

        tracks = [track]

        database_response = self.table.update(tracks)

        return database_response[0]

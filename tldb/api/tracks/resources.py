from flask import request
from flask.views import MethodView

from tldb.api.tracks import models
from tldb.api.tracks.models import blp
from tldb.database.track import Track as TrackTable


@blp.route("")
class Tracks(MethodView):
    def __init__(self):
        self.table = TrackTable()

    @blp.response(200, models.GetTrackSchema(many=True))
    def get(self):
        """
        List all tracks
        """
        verbose = request.args.get("verbose") == "1"

        database_response = self.table.get(verbose=verbose)

        return list(database_response)

    @blp.arguments(models.CreateTrackSchema)
    def post(self, post_data):
        """
        Create a new track
        """
        database_response = self.table.insert(post_data)
        track_id = database_response[0]

        return track_id

    @blp.arguments(models.UpdateTrackSchema(many=True))
    @blp.response(200, models.GetTrackSchema(many=True))
    def patch(self, patch_data):
        """
        Create or update a set of tracks
        """
        database_response = self.table.upsert(patch_data)

        return database_response


@blp.route("/<string:id>")
class Track(MethodView):
    def __init__(self):
        self.table = TrackTable()

    @blp.response(200, models.GetTrackSchema)
    def get(self, id):
        """
        Get a single track
        """
        verbose = request.args.get("verbose") == "1"

        database_response = self.table.get(id, verbose=verbose)

        return database_response

    @blp.arguments(models.CreateTrackSchema)
    @blp.response(200, models.GetTrackSchema)
    def put(self, put_data, id):
        """
        Update a single track
        """
        schema = models.CreateTrackSchema()
        json_data = schema.dump(put_data)

        json_data["id"] = id

        database_response = self.table.update([json_data])

        return database_response[0]

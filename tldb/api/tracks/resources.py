from flask import request
from flask_restx import Resource, marshal

from tldb.api.tracks import models
from tldb.api.tracks.models import api
from tldb.database.track import Track as TrackTable


@api.route("")
class Tracks(Resource):
    def __init__(self, res):
        super().__init__(res)

        self.table = TrackTable()

    def get(self):
        """
        List all tracks
        """
        database_response = self.table.get()

        return list(database_response)

    @api.expect(models.track)
    def post(self):
        """
        Create a new track
        """
        api_model = marshal(api.payload, models.track)

        del api_model["id"]

        database_response = self.table.insert(api_model)
        track_id = database_response[0]

        return track_id

    @api.expect(models.tracks)
    def patch(self):
        """
        Create or update a set of tracks
        """
        api_model = marshal(api.payload, models.tracks)

        database_response = self.table.upsert(api_model.get("tracks"))

        return database_response


@api.route("/<string:id>")
class Track(Resource):
    def __init__(self, res):
        super().__init__(res)

        self.table = TrackTable()

    def get(self, id):
        """
        Get a single track
        """
        if request.args.get("verbose") == "1":
            database_response = self.table.get(id, True)
        else:
            database_response = self.table.get(id)

        return database_response

    @api.expect(models.track)
    def put(self, id):
        """
        Update a single track
        """
        api_model = marshal(api.payload, models.track)

        api_model["id"] = id

        database_response = self.table.update([api_model])

        return list(database_response)

from flask_restx import Resource, marshal

from tldb.api.track import models
from tldb.api.track.models import api
from tldb.database import tables


@api.route("")
class Tracks(Resource):
    def __init__(self, res):
        super().__init__(res)

        self.table = tables.Track()

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

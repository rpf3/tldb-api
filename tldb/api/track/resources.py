from flask_restx import Resource

from tldb.api.track.models import api
from tldb.database import tables


@api.route("")
class Tracks(Resource):
    def get(self):
        """
        List all tracks
        """
        track_table = tables.Track()

        database_response = track_table.get()

        return list(database_response)

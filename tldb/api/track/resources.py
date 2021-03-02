from flask_restx import Resource

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

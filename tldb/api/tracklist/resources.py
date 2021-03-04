from flask_restx import Resource

from tldb.api.tracklist.models import api
from tldb.database.tracklist import Tracklist as TracklistTable


@api.route("")
class Tracklists(Resource):
    def __init__(self, res):
        super().__init__(res)

        self.table = TracklistTable()

    def get(self):
        """
        List all tracklists
        """
        database_response = self.table.get()

        return list(database_response)

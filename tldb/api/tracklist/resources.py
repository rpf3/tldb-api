from flask_restx import Resource

from tldb.api.tracklist.models import api
from tldb.database import tables


@api.route("")
class Tracklists(Resource):
    def get(self):
        """
        List all tracklists
        """
        tracklist_table = tables.Tracklist()

        database_response = tracklist_table.get()

        return list(database_response)

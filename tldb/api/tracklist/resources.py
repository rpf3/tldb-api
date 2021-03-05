from flask_restx import Resource, marshal

from tldb.api.tracklist import models
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

    @api.expect(models.tracklist)
    def post(self):
        """
        Create a new tracklist
        """
        api_model = marshal(api.payload, models.tracklist)

        del api_model["id"]

        database_response = self.table.insert(api_model)
        tracklist_id = database_response[0]

        return tracklist_id

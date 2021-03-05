from flask import request
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

    @api.expect(models.tracklists)
    def patch(self):
        """
        Create or update a set of tracklists
        """
        api_model = marshal(api.payload, models.tracklists)

        insert_models = []
        update_models = []

        for tracklist in api_model.get("tracklists"):
            if tracklist["id"] is None:
                del tracklist["id"]

                insert_models.append(tracklist)
            else:
                update_models.append(tracklist)

        new_tracklist_ids = self.table.insert(insert_models)
        update_tracklist_ids = self.table.update(update_models)

        tracklist_ids = new_tracklist_ids + update_tracklist_ids

        return tracklist_ids


@api.route("/<string:id>")
class Tracklist(Resource):
    def __init__(self, res):
        super().__init__(res)

        self.table = TracklistTable()

    def get(self, id):
        """
        Get a single tracklist
        """
        if request.args.get("verbose") == "1":
            database_response = self.table.get(id, True)
        else:
            database_response = self.table.get(id)

        return database_response

    @api.expect(models.tracklist)
    def put(self, id):
        """
        Update a single tracklist
        """
        api_model = marshal(api.payload, models.tracklist)

        api_model["id"] = id

        database_response = self.table.update([api_model])

        return list(database_response)

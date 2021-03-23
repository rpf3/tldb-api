from flask import request
from flask.views import MethodView

from tldb.api.tracklists import models
from tldb.api.tracklists.models import blp
from tldb.database.tracklist import Tracklist as TracklistTable


@blp.route("")
class Tracklists(MethodView):
    def __init__(self):
        self.table = TracklistTable()

    @blp.response(200, models.GetTracklistSchema(many=True))
    def get(self):
        """
        List all tracklists
        """
        skip = int(request.args.get("skip", 0))
        take = int(request.args.get("take", 10))
        verbose = request.args.get("verbose") == "1"

        database_response = self.table.get(skip=skip, take=take, verbose=verbose)

        # print(database_response)

        return list(database_response)

    @blp.arguments(models.CreateTracklistSchema)
    def post(self, post_data):
        """
        Create a new tracklist
        """
        database_response = self.table.insert(post_data)
        tracklist_id = database_response[0]

        return tracklist_id

    @blp.arguments(models.UpdateTracklistSchema(many=True))
    @blp.response(200, models.GetTracklistSchema(many=True))
    def patch(self, patch_data):
        """
        Create or update a set of tracklists
        """
        database_response = self.table.upsert(patch_data)

        return database_response


@blp.route("/<string:id>")
class Tracklist(MethodView):
    def __init__(self):
        self.table = TracklistTable()

    @blp.response(200, models.GetTracklistSchema)
    def get(self, id):
        """
        Get a single tracklist
        """
        verbose = request.args.get("verbose") == "1"

        database_response = self.table.get(id, verbose=verbose)

        return database_response

    @blp.arguments(models.CreateTracklistSchema)
    @blp.response(200, models.GetTracklistSchema)
    def put(self, put_data, id):
        """
        Update a single tracklist
        """
        schema = models.CreateTracklistSchema()
        json_data = schema.dump(put_data)

        json_data["id"] = id

        database_response = self.table.update([json_data])

        return database_response[0]

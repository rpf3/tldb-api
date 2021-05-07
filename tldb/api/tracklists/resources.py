from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint

from tldb import database, models
from tldb.api import utils

blp = Blueprint("tracklists", "tracklists", url_prefix="/tracklists")


@blp.route("")
class Tracklists(MethodView):
    def __init__(self):
        self.table = database.TracklistTable()

    @blp.response(200, models.TracklistSchema(many=True))
    def get(self):
        """
        List all tracklists
        """
        query = request.args.get("query")
        params = utils.parse_search_args(request)

        database_response = self.table.search(query=query, params=params)

        return database_response

    @blp.arguments(models.TracklistWriteSchema)
    @blp.response(200, models.TracklistSchema)
    def post(self, tracklist):
        """
        Create a new tracklist
        """
        tracklists = [tracklist]
        database_response = self.table.insert(tracklists)

        return database_response[0]

    @blp.arguments(models.TracklistSchema(many=True))
    @blp.response(200, models.TracklistSchema(many=True))
    def patch(self, tracklists):
        """
        Create or update a set of tracklists
        """
        database_response = self.table.upsert(tracklists)

        return database_response


@blp.route("/<string:id>")
class TracklistsById(MethodView):
    def __init__(self):
        self.table = database.TracklistTable()

    @blp.response(200, models.TracklistSchema)
    def get(self, id):
        """
        Get a single tracklist
        """
        verbose = request.args.get("verbose") == "1"

        ids = [id]

        database_response = self.table.get(ids, verbose=verbose)

        return database_response[0]

    @blp.arguments(models.TracklistWriteSchema)
    @blp.response(200, models.TracklistSchema)
    def put(self, tracklist, id):
        """
        Update a single tracklist
        """
        tracklist.id = id

        tracklists = [tracklist]

        database_response = self.table.update(tracklists)

        return database_response[0]

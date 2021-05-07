from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint

from tldb.api import utils
from tldb.database import TracklistTable
from tldb.models import TracklistSchema, TracklistWriteSchema

blp = Blueprint("tracklists", "tracklists", url_prefix="/tracklists")


@blp.route("")
class Tracklists(MethodView):
    def __init__(self):
        self.table = TracklistTable()

    @blp.response(200, TracklistSchema(many=True))
    def get(self):
        """
        List all tracklists
        """
        query = request.args.get("query")
        params = utils.parse_search_args(request)

        database_response = self.table.search(query=query, params=params)

        return database_response

    @blp.arguments(TracklistWriteSchema)
    @blp.response(200, TracklistSchema)
    def post(self, tracklist):
        """
        Create a new tracklist
        """
        tracklists = [tracklist]
        database_response = self.table.insert(tracklists)

        return database_response[0]

    @blp.arguments(TracklistSchema(many=True))
    @blp.response(200, TracklistSchema(many=True))
    def patch(self, tracklists):
        """
        Create or update a set of tracklists
        """
        database_response = self.table.upsert(tracklists)

        return database_response


@blp.route("/<string:id>")
class TracklistsById(MethodView):
    def __init__(self):
        self.table = TracklistTable()

    @blp.response(200, TracklistSchema)
    def get(self, id):
        """
        Get a single tracklist
        """
        verbose = request.args.get("verbose") == "1"

        ids = [id]

        database_response = self.table.get(ids, verbose=verbose)

        return database_response[0]

    @blp.arguments(TracklistWriteSchema)
    @blp.response(200, TracklistSchema)
    def put(self, tracklist, id):
        """
        Update a single tracklist
        """
        tracklist.id = id

        tracklists = [tracklist]

        database_response = self.table.update(tracklists)

        return database_response[0]

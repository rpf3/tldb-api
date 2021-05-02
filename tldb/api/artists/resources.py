from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint

from tldb.database import ArtistTable, TracklistTable, TrackTable
from tldb.models import ArtistSchema, ArtistWriteSchema, TracklistSchema, TrackSchema

blp = Blueprint("artists", "artists", url_prefix="/artists")


@blp.route("")
class Artists(MethodView):
    def __init__(self):
        self.table = ArtistTable()

    @blp.response(200, ArtistSchema(many=True))
    def get(self):
        """
        List all artists
        """
        database_response = self.table.search(skip=0, take=10, query=None)

        return database_response

    @blp.arguments(ArtistWriteSchema)
    @blp.response(200, ArtistSchema)
    def post(self, artist):
        """
        Create a new artist
        """
        artists = [artist]
        database_response = self.table.insert(artists)

        return database_response[0]

    @blp.arguments(ArtistSchema(many=True))
    @blp.response(200, ArtistSchema(many=True))
    def patch(self, artists):
        """
        Create or update a set of artists
        """
        database_response = self.table.upsert(artists)

        return database_response


@blp.route("/<string:id>")
class ArtistsById(MethodView):
    def __init__(self):
        self.table = ArtistTable()

    @blp.response(200, ArtistSchema)
    def get(self, id):
        """
        Get a single artist
        """
        ids = [id]

        database_response = self.table.get(ids)

        return database_response[0]

    @blp.arguments(ArtistWriteSchema)
    @blp.response(200, ArtistSchema)
    def put(self, artist, id):
        """
        Update a single artist
        """
        artist.id = id

        artists = [artist]

        database_response = self.table.update(artists)

        return database_response[0]


@blp.route("/<string:id>/tracklists")
class TracklistsByArtistId(MethodView):
    def __init__(self):
        self.table = TracklistTable()

    @blp.response(200, TracklistSchema(many=True))
    def get(self, id):
        """
        Get all tracklists by a single artist
        """
        skip = int(request.args.get("skip", 0))
        take = int(request.args.get("take", 10))

        database_response = self.table.get_all_by_artist(id, skip=skip, take=take)

        return database_response


@blp.route("/<string:id>/tracks")
class TracksByArtistId(MethodView):
    def __init__(self):
        self.table = TrackTable()

    @blp.response(200, TrackSchema(many=True))
    def get(self, id):
        """
        Get all tracklists by a single artist
        """
        skip = int(request.args.get("skip", 0))
        take = int(request.args.get("take", 10))
        verbose = request.args.get("verbose") == "1"

        database_response = self.table.get_all_by_artist(
            id, skip=skip, take=take, verbose=verbose
        )

        return database_response

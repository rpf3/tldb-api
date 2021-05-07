from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint

from tldb import database, models
from tldb.api import utils

blp = Blueprint("artists", "artists", url_prefix="/artists")


@blp.route("")
class Artists(MethodView):
    def __init__(self):
        self.table = database.ArtistTable()

    @blp.response(200, models.ArtistSchema(many=True))
    def get(self):
        """
        List all artists
        """
        params = utils.parse_search_args(request)

        database_response = self.table.search(query=None, params=params)

        return database_response

    @blp.arguments(models.ArtistWriteSchema)
    @blp.response(200, models.ArtistSchema)
    def post(self, artist):
        """
        Create a new artist
        """
        artists = [artist]
        database_response = self.table.insert(artists)

        return database_response[0]

    @blp.arguments(models.ArtistSchema(many=True))
    @blp.response(200, models.ArtistSchema(many=True))
    def patch(self, artists):
        """
        Create or update a set of artists
        """
        database_response = self.table.upsert(artists)

        return database_response


@blp.route("/<string:id>")
class ArtistsById(MethodView):
    def __init__(self):
        self.table = database.ArtistTable()

    @blp.response(200, models.ArtistSchema)
    def get(self, id):
        """
        Get a single artist
        """
        ids = [id]

        database_response = self.table.get(ids)

        return database_response[0]

    @blp.arguments(models.ArtistWriteSchema)
    @blp.response(200, models.ArtistSchema)
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
        self.table = database.TracklistTable()

    @blp.response(200, models.TracklistSchema(many=True))
    def get(self, id):
        """
        Get all tracklists by a single artist
        """
        params = utils.parse_search_args(request)

        database_response = self.table.get_all_by_artist(id, params)

        return database_response


@blp.route("/<string:id>/tracks")
class TracksByArtistId(MethodView):
    def __init__(self):
        self.table = database.TrackTable()

    @blp.response(200, models.TrackSchema(many=True))
    def get(self, id):
        """
        Get all tracklists by a single artist
        """
        params = utils.parse_search_args(request)

        database_response = self.table.get_all_by_artist(id, params)

        return database_response

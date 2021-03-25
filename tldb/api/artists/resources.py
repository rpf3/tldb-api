from flask.views import MethodView
from flask_smorest import Blueprint

from tldb.database.artist import Artist as ArtistTable
from tldb.models import ArtistSchema

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
        database_response = self.table.get()

        return database_response

    @blp.arguments(ArtistSchema(exclude=["id"]))
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
class Artist(MethodView):
    def __init__(self):
        self.table = ArtistTable()

    @blp.response(200, ArtistSchema)
    def get(self, id):
        """
        Get a single artist
        """
        database_response = self.table.get(id)

        return database_response[0]

    @blp.arguments(ArtistSchema(exclude=["id"]))
    @blp.response(200, ArtistSchema)
    def put(self, artist, id):
        """
        Update a single artist
        """
        artist.id = id

        artists = [artist]

        database_response = self.table.update(artists)

        return database_response[0]

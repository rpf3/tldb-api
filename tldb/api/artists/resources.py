from flask.views import MethodView

from tldb.api.artists import models
from tldb.api.artists.models import blp
from tldb.database.artist import Artist as ArtistTable


@blp.route("")
class Artists(MethodView):
    def __init__(self):
        self.table = ArtistTable()

    @blp.response(200, models.GetArtistSchema(many=True))
    def get(self):
        """
        List all artists
        """
        database_response = self.table.get()

        return list(database_response)

    @blp.arguments(models.CreateArtistSchema)
    def post(self, post_data):
        """
        Create a new artist
        """
        database_response = self.table.insert(post_data)
        artist_id = database_response[0]

        return artist_id

    @blp.arguments(models.UpdateArtistSchema(many=True))
    @blp.response(200, models.GetArtistSchema(many=True))
    def patch(self, patch_data):
        """
        Create or update a set of artists
        """
        database_response = self.table.upsert(patch_data)

        return database_response


@blp.route("/<string:id>")
class Artist(MethodView):
    def __init__(self):
        self.table = ArtistTable()

    @blp.response(200, models.GetArtistSchema)
    def get(self, id):
        """
        Get a single artist
        """
        database_response = self.table.get(id)

        return database_response

    @blp.arguments(models.CreateArtistSchema)
    @blp.response(200, models.GetArtistSchema)
    def put(self, put_data, id):
        """
        Update a single artist
        """
        schema = models.CreateArtistSchema()
        json_data = schema.dump(put_data)

        json_data["id"] = id

        database_response = self.table.update([json_data])

        return database_response[0]

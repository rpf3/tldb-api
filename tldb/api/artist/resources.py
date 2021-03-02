from flask_restx import Resource, marshal

from tldb.api.artist import models
from tldb.api.artist.models import api
from tldb.database import tables


@api.route("")
class Artists(Resource):
    def get(self):
        """
        List all artists
        """
        artist_table = tables.Artist()

        database_response = artist_table.get()

        return list(database_response)

    @api.expect(models.artist)
    def post(self):
        """
        Create a new artist
        """
        artist_table = tables.Artist()

        api_model = marshal(api.payload, models.artist)

        del api_model["id"]

        database_response = artist_table.insert(api_model)
        artist_id = database_response[0]

        return artist_id

    @api.expect(models.artists)
    def patch(self):
        """
        Create or update a set of artists
        """
        api_model = marshal(api.payload, models.artists)

        return api_model


@api.route("/<string:id>")
class Artist(Resource):
    def get(self, id):
        """
        Get a single artist
        """
        artist_table = tables.Artist()

        database_response = artist_table.get(id)

        return database_response

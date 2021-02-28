from flask_restx import Resource, marshal

from tldb.api.artist import models
from tldb.api.artist.models import api


@api.route("")
class Artists(Resource):
    def get(self):
        """
        List all artists
        """
        return []

    @api.expect(models.artist)
    def post(self):
        """
        Create a new artist
        """
        api_model = marshal(api.payload, models.artist)

        return api_model

    @api.expect(models.artists)
    def patch(self):
        """
        Create or update a set of artists
        """
        api_model = marshal(api.payload, models.artists)

        return api_model

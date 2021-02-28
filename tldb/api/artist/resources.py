from flask_restx import Resource, marshal

from tldb.api.artist.models import api, artist


@api.route("")
class Artists(Resource):
    def get(self):
        """
        List all artists
        """
        return []

    @api.expect(artist)
    def post(self):
        """
        Create a new artist
        """
        api_model = marshal(api.payload, artist)

        return api_model

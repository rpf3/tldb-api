from flask_restx import Resource

from tldb.api.artist.models import api


@api.route("")
class Artists(Resource):
    def get(self):
        """
        List all artists
        """
        return []

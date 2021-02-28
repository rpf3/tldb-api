from flask_restx import Resource

from tldb.api.track.models import api


@api.route("")
class Tracks(Resource):
    def get(self):
        """
        List all tracks
        """
        return []

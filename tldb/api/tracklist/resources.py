from flask_restx import Resource

from tldb.api.tracklist.models import api


@api.route("")
class Tracklists(Resource):
    def get(self):
        """
        List all tracklists
        """
        return []

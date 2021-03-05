from flask_restx import Resource, marshal

from tldb.api.imports import models, utils
from tldb.api.imports.models import api


@api.route("")
class Imports(Resource):
    @api.expect(models.tracklists)
    def post(self):
        """
        Import a set of tracklists and related data
        """
        api_model = marshal(api.payload, models.tracklists)

        tracklists = api_model.get("tracklists")

        artists = []
        tracks = []

        # Get the artist and tracks from each tracklist
        for tracklist in tracklists:
            artists.append(tracklist.get("artist"))

            tracks += tracklist.get("tracks")

        # Get the artist from each track in the tracklists
        for track in tracks:
            artists.append(track.get("artist"))

        artist_map = utils.create_artists(artists)
        track_map = utils.create_tracks(tracks, artist_map)

        database_response = utils.create_tracklists(tracklists, artist_map, track_map)

        return database_response

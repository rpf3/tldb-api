from flask.views import MethodView

from tldb.api.imports import models, utils
from tldb.api.imports.models import blp
from tldb.api.tracklists.models import GetTracklistSchema


@blp.route("")
class Imports(MethodView):
    @blp.arguments(models.ImportTracklistSchema(many=True))
    @blp.response(200, GetTracklistSchema(many=True))
    def post(self, post_data):
        """
        Import a set of tracklists and related data
        """
        artists = []
        tracks = []

        # Get the artist and tracks from each tracklist
        for tracklist in post_data:
            artists.extend(tracklist.get("artists"))
            tracks.extend(tracklist.get("tracks"))

        # Get the artist from each track in the tracklists
        for track in tracks:
            artists.append(track.get("artist"))

            remix = track.get("remix")

            if remix is not None:
                remix_artist = remix.get("artist")

                if remix_artist:
                    artists.append(remix_artist)

        artist_map = utils.create_artists(artists)
        track_map = utils.create_tracks(tracks, artist_map)

        database_response = utils.create_tracklists(post_data, artist_map, track_map)

        return database_response

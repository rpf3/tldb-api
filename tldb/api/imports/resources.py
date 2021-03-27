from flask.views import MethodView
from flask_smorest import Blueprint

from tldb.api.imports import utils
from tldb.models import TracklistImportSchema, TracklistSchema

blp = Blueprint("imports", "imports", url_prefix="/imports")


@blp.route("")
class Imports(MethodView):
    @blp.arguments(TracklistImportSchema(many=True))
    @blp.response(200, TracklistSchema(many=True))
    def post(self, post_data):
        """
        Import a set of tracklists and related data
        """
        artists = []
        tracks = []

        # Get the artist and tracks from each tracklist
        for tracklist in post_data:
            artists.extend(tracklist.artists)
            tracks.extend([x.track for x in tracklist.tracks])

        # Get the artist from each track in the tracklists
        for track in tracks:
            artists.append(track.artist)

            remix = track.remix

            if remix is not None:
                remix_artist = remix.artist

                if remix_artist:
                    artists.append(remix_artist)

        artist_map = utils.create_artists(artists)
        track_map = utils.create_tracks(tracks, artist_map)

        database_response = utils.create_tracklists(post_data, artist_map, track_map)

        return database_response

from flask_restx import Namespace, fields

api = Namespace("imports")


artist = api.model(
    "Artist", {"name": fields.String(description="The name of the artist")}
)

track = api.model(
    "Track",
    {
        "name": fields.String(description="The name of the track"),
        "index": fields.Integer(description="The index in the tracklist"),
        "artist": fields.Nested(artist),
    },
)

tracklist = api.model(
    "Tracklist",
    {
        "name": fields.String(description="The name of the tracklist"),
        "artist": fields.Nested(artist),
        "tracks": fields.List(fields.Nested(track)),
    },
)

tracklists = api.model(
    "Tracklists", {"tracklists": fields.List(fields.Nested(tracklist))}
)

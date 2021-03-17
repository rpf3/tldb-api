from flask_restx import Namespace, fields

api = Namespace("imports")


artist = api.model(
    "Artist",
    {"name": fields.String(description="The name of the artist", default="ID")},
)

remix = api.model(
    "Remix",
    {
        "name": fields.String(description="The name of the remix"),
        "artist": fields.Nested(artist),
    },
)

track = api.model(
    "Track",
    {
        "name": fields.String(description="The name of the track", default="ID"),
        "index": fields.Integer(description="The index in the tracklist"),
        "artist": fields.Nested(artist),
        "remix": fields.Nested(remix, allow_null=True),
    },
)

tracklist = api.model(
    "Tracklist",
    {
        "name": fields.String(description="The name of the tracklist"),
        "date": fields.Date(description="The date of the tracklist"),
        "artists": fields.List(fields.Nested(artist)),
        "tracks": fields.List(fields.Nested(track)),
    },
)

tracklists = api.model(
    "Tracklists", {"tracklists": fields.List(fields.Nested(tracklist))}
)

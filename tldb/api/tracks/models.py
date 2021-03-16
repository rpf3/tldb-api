from flask_restx import Namespace, fields

api = Namespace("tracks")

remix = api.model(
    "Remix",
    {
        "name": fields.String(description="The name of the remix"),
        "artistId": fields.String(description="The ID of the artist"),
    },
)

track = api.model(
    "Track",
    {
        "id": fields.String(description="The ID of the track", readonly=True),
        "name": fields.String(description="The name of the track"),
        "artistId": fields.String(description="The ID of the artist"),
        "remix": fields.Nested(remix, allow_null=True),
    },
)

tracks = api.model("Tracks", {"tracks": fields.List(fields.Nested(track))})

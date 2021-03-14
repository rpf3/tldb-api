from flask_restx import Namespace, fields

api = Namespace("tracklists")

track = api.model(
    "Track",
    {
        "id": fields.String(description="The ID of the track"),
        "index": fields.Integer(description="The index in the tracklist"),
    },
)

tracklist = api.model(
    "Tracklist",
    {
        "id": fields.String(description="The ID of the tracklist", readonly=True),
        "name": fields.String(description="The name of the tracklist"),
        "artistIds": fields.List(fields.String(description="The ID of the artist")),
        "tracks": fields.List(fields.Nested(track)),
    },
)

tracklists = api.model(
    "Tracklists", {"tracklists": fields.List(fields.Nested(tracklist))}
)

from flask_restx import Namespace, fields

api = Namespace("tracklists")

tracklist = api.model(
    "Tracklist",
    {
        "id": fields.String(description="The ID of the tracklist", readonly=True),
        "name": fields.String(description="The name of the tracklist"),
        "artistId": fields.String(description="The ID of the artist"),
        "tracks": fields.List(fields.String(description="The ID of the track")),
    },
)

tracklists = api.model(
    "Tracklists", {"tracklists": fields.List(fields.Nested(tracklist))}
)

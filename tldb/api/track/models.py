from flask_restx import Namespace, fields

api = Namespace("tracks")

track = api.model(
    "Track",
    {
        "id": fields.String(description="The ID of the track", readonly=True),
        "name": fields.String(description="The name of the track"),
        "artistId": fields.String(description="The ID of the artist"),
    },
)

from flask_restx import Namespace, fields

api = Namespace("artists")

artist = api.model(
    "Artist",
    {
        "id": fields.String(description="The ID of the artist", readonly=True),
        "name": fields.String(description="The name of the artist"),
    },
)

artists = api.model("Artists", {"artists": fields.List(fields.Nested(artist))})

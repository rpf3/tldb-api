from flask_restx import Namespace, fields

api = Namespace("artists")

artist = api.model(
    "Artist",
    {
        "id": fields.String(description="The ID of the artist"),
        "name": fields.String(description="The name of the artist"),
    },
)

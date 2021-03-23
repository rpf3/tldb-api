from flask_smorest import Blueprint
from marshmallow import Schema, fields

blp = Blueprint("imports", "imports", url_prefix="/imports")


class ImportArtistSchema(Schema):
    name = fields.String(description="The name of the artist", default="ID")


class ImportRemixSchema(Schema):
    name = fields.String(description="The name of the remix")
    artist = fields.Nested(ImportArtistSchema, allow_none=True)


class ImportTrackSchema(Schema):
    name = fields.String(description="The name of the track", default="ID")
    index = fields.Integer(description="The index in the tracklist")
    artist = fields.Nested(ImportArtistSchema)
    remix = fields.Nested(ImportRemixSchema, allow_none=True)


class ImportTracklistSchema(Schema):
    name = fields.String(description="The name of the track")
    artists = fields.List(fields.Nested(ImportArtistSchema))
    tracks = fields.List(fields.Nested(ImportTrackSchema))

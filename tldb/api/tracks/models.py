from flask_smorest import Blueprint
from marshmallow import Schema, fields

from tldb.api.artists.models import GetArtistSchema

blp = Blueprint("tracks", "tracks", url_prefix="/tracks")


class RemixSchema(Schema):
    name = fields.String(description="The name of the remix")
    artistId = fields.String(description="The ID of the artist")
    artist = fields.Nested(GetArtistSchema, dump_only=True)


class CreateTrackSchema(Schema):
    name = fields.String(description="The name of the track")
    artistId = fields.String(description="The ID of the artist")
    remix = fields.Nested(RemixSchema, allow_none=True)


class GetTrackSchema(CreateTrackSchema):
    id = fields.String(description="The ID of the track", dump_only=True)
    artist = fields.Nested(GetArtistSchema, dump_only=True)


class UpdateTrackSchema(CreateTrackSchema):
    id = fields.String(description="The ID of the track")

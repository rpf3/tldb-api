from flask_smorest import Blueprint
from marshmallow import Schema, fields

from tldb.api.artists.models import GetArtistSchema
from tldb.api.tracks.models import GetTrackSchema

blp = Blueprint("tracklists", "tracklists", url_prefix="/tracklists")


class CreateIndexedTrackSchema(Schema):
    id = fields.String(description="The ID of the track")
    index = fields.Integer(description="The index in the tracklist")


class GetIndexedTrackSchema(GetTrackSchema):
    index = fields.Integer(description="The index in the tracklist")


class CreateTracklistSchema(Schema):
    id = fields.String(description="The ID of the tracklist", dump_only=True)
    name = fields.String(description="The name of the tracklist")
    artistIds = fields.List(fields.String(description="The ID of the artist"))
    tracks = fields.List(fields.Nested(CreateIndexedTrackSchema))


class GetTracklistSchema(CreateTracklistSchema):
    id = fields.String(description="The ID of the tracklist", dump_only=True)
    artists = fields.List(fields.Nested(GetArtistSchema), dump_only=True)
    tracks = fields.List(fields.Nested(GetIndexedTrackSchema), dump_only=True)


class UpdateTracklistSchema(CreateTracklistSchema):
    id = fields.String(description="The ID of the tracklist")

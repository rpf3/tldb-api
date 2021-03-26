from marshmallow import EXCLUDE, fields, post_load

from tldb.models.artist import ArtistIdSchema, ArtistSchema
from tldb.models.schema import BaseSchema


class Remix:
    def __init__(self, name, artist):
        self.name = name
        self.artist = artist


class RemixSchema(BaseSchema):
    name = fields.String(description="The name of the remix")
    artist = fields.Nested(ArtistSchema)

    @post_load
    def create_remix(self, data, **kwargs):
        return Remix(**data)

    class Meta:
        unknown = EXCLUDE


class RemixWriteSchema(RemixSchema):
    artist = fields.Nested(ArtistIdSchema)


class Track:
    def __init__(self, name=None, artist=None, remix=None, id=None):
        self.id = id
        self.artist = artist
        self.name = name
        self.remix = remix


class TrackSchema(BaseSchema):
    id = fields.String(description="The ID of the track")
    name = fields.String(description="The name of the track")
    artist = fields.Nested(ArtistSchema)
    remix = fields.Nested(RemixSchema, allow_none=True)

    @post_load
    def create_track(self, data, **kwargs):
        return Track(**data)


class TrackWriteSchema(TrackSchema):
    artist = fields.Nested(ArtistIdSchema)
    remix = fields.Nested(RemixWriteSchema, allow_none=True)

    class Meta:
        exclude = ["id"]


class TrackIdSchema(TrackSchema):
    class Meta:
        fields = ["id"]

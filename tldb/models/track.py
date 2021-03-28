import json

from marshmallow import EXCLUDE, fields, post_load

from tldb.models.artist import ArtistIdSchema, ArtistSchema, ArtistWriteSchema
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


class RemixWriteSchema(RemixSchema):
    artist = fields.Nested(ArtistIdSchema)


class RemixImportSchema(RemixSchema):
    artist = fields.Nested(ArtistWriteSchema)

    class Meta:
        unknown = EXCLUDE


class Track:
    def __init__(self, name=None, artist=None, remix=None, id=None, original_id=None):
        self.id = id
        self.artist = artist
        self.name = name
        self.remix = remix
        self.original_id = original_id

    def get_unique_hash(self):
        obj = {"name": self.name, "artistId": self.artist.id}

        if self.remix is not None:
            obj["remixName"] = self.remix.name
            obj["remixArtistId"] = self.remix.artist.id

        result = hash(json.dumps(obj, sort_keys=True))

        return result


class TrackSchema(BaseSchema):
    id = fields.String(description="The ID of the track")
    name = fields.String(description="The name of the track")
    artist = fields.Nested(ArtistSchema)
    remix = fields.Nested(RemixSchema, allow_none=True)
    original_id = fields.String(
        description="The ID of the original track", data_key="originalId"
    )

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


class TrackImportSchema(TrackSchema):
    artist = fields.Nested(ArtistWriteSchema)
    remix = fields.Nested(RemixImportSchema, allow_none=True)

    class Meta:
        exclude = ["id"]
        unknown = EXCLUDE

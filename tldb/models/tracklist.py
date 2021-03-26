from marshmallow import fields, post_load

from tldb.models.artist import ArtistIdSchema, ArtistSchema
from tldb.models.schema import BaseSchema
from tldb.models.track import TrackIdSchema, TrackSchema


class IndexedTrack:
    def __init__(self, index, track):
        self.index = index
        self.track = track


class IndexedTrackSchema(BaseSchema):
    index = fields.Integer(description="The index in the tracklist")
    track = fields.Nested(TrackSchema)

    @post_load
    def create_indexed_track(self, data, **kwargs):
        return IndexedTrack(**data)


class IndexedTrackWriteSchema(IndexedTrackSchema):
    track = fields.Nested(TrackIdSchema)


class Tracklist:
    def __init__(self, name=None, artists=None, tracks=None, id=None):
        self.id = id
        self.name = name
        self.tracks = tracks
        self.artists = artists


class TracklistSchema(BaseSchema):
    id = fields.String(description="The ID of the tracklist")
    name = fields.String(description="The name of the tracklist")
    artists = fields.List(fields.Nested(ArtistSchema))
    tracks = fields.List(fields.Nested(IndexedTrackSchema), allow_none=True)

    @post_load
    def create_tracklist(self, data, **kwargs):
        return Tracklist(**data)


class TracklistWriteSchema(TracklistSchema):
    artists = fields.List(fields.Nested(ArtistIdSchema))
    tracks = fields.List(fields.Nested(IndexedTrackWriteSchema), allow_none=True)

    class Meta:
        exclude = ["id"]

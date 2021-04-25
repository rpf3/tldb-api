from marshmallow import EXCLUDE, fields, post_load

from tldb.models.artist import ArtistIdSchema, ArtistSchema, ArtistWriteSchema
from tldb.models.schema import BaseSchema
from tldb.models.track import TrackIdSchema, TrackImportSchema, TrackSchema


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


class IndexedTrackImportSchema(IndexedTrackSchema):
    track = fields.Nested(TrackImportSchema)

    class Meta:
        unknown = EXCLUDE


class Tracklist:
    def __init__(
        self,
        name=None,
        date=None,
        series=None,
        artists=None,
        tracks=None,
        tags=None,
        id=None,
    ):
        self.id = id
        self.name = name
        self.date = date
        self.series = series
        self.tracks = tracks
        self.artists = artists
        self.tags = tags


class TracklistSchema(BaseSchema):
    id = fields.String(description="The ID of the tracklist")
    name = fields.String(description="The name of the tracklist")
    date = fields.Date(description="The date of the tracklist")
    series = fields.String(
        description="The series of the tracklist, if any", allow_none=True
    )
    artists = fields.List(fields.Nested(ArtistSchema))
    tracks = fields.List(fields.Nested(IndexedTrackSchema), allow_none=True)
    tags = fields.List(fields.String(), description="A list of tags")

    @post_load
    def create_tracklist(self, data, **kwargs):
        return Tracklist(**data)


class TracklistWriteSchema(TracklistSchema):
    artists = fields.List(fields.Nested(ArtistIdSchema))
    tracks = fields.List(fields.Nested(IndexedTrackWriteSchema), allow_none=True)

    class Meta:
        exclude = ["id"]


class TracklistImportSchema(TracklistSchema):
    artists = fields.List(fields.Nested(ArtistWriteSchema))
    tracks = fields.List(fields.Nested(IndexedTrackImportSchema))

    class Meta:
        exclude = ["id"]
        unknown = EXCLUDE

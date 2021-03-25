from marshmallow import Schema, fields, post_load

from tldb.models import ArtistSchema, TrackSchema


class IndexedTrack:
    def __init__(self, id, index, track=None):
        self.id = id
        self.index = index
        self.track = track


class IndexedTrackSchema(Schema):
    id = fields.String(description="The ID of the track")
    index = fields.Integer(description="The index in the tracklist")
    track = fields.Nested(TrackSchema, allow_none=True)

    @post_load
    def create_indexed_track(self, data, **kwargs):
        return IndexedTrack(**data)


class Tracklist:
    def __init__(self, name=None, artist_ids=None, tracks=None, id=None, artists=None):
        self.id = id
        self.name = name
        self.artist_ids = artist_ids
        self.tracks = tracks
        self.artists = artists


class TracklistSchema(Schema):
    id = fields.String(description="The ID of the tracklist")
    name = fields.String(description="The name of the tracklist")
    artist_ids = fields.List(
        fields.String(description="The ID of the artist"), data_key="artistIds"
    )
    tracks = fields.List(fields.Nested(IndexedTrackSchema), allow_none=True)
    artists = fields.List(fields.Nested(ArtistSchema), allow_none=True)

    @post_load
    def create_tracklist(self, data, **kwargs):
        return Tracklist(**data)


class WriteTracklistSchema(TracklistSchema):
    class Meta:
        exclude = ["id", "artists", "tracks.track"]

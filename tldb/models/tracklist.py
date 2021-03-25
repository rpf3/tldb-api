from marshmallow import Schema, fields, post_load


class IndexedTrack:
    def __init__(self, id, index):
        self.id = id
        self.index = index


class IndexedTrackSchema(Schema):
    id = fields.String(description="The ID of the track")
    index = fields.Integer(description="The index in the tracklist")

    @post_load
    def create_indexed_track(self, data, **kwargs):
        return IndexedTrack(**data)


class Tracklist:
    def __init__(self, name=None, artist_ids=None, tracks=None, id=None):
        self.id = id
        self.name = name
        self.artist_ids = artist_ids
        self.tracks = tracks


class TracklistSchema(Schema):
    id = fields.String(description="The ID of the tracklist")
    name = fields.String(description="The name of the tracklist")
    artist_ids = fields.List(
        fields.String(description="The ID of the artist"), data_key="artistIds"
    )
    tracks = fields.List(fields.Nested(IndexedTrackSchema))

    @post_load
    def create_tracklist(self, data, **kwargs):
        return Tracklist(**data)


class WriteTracklistSchema(TracklistSchema):
    class Meta:
        exclude = ["id"]

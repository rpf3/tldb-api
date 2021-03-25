from marshmallow import EXCLUDE, Schema, fields, post_load


class Remix:
    def __init__(self, name, artist_id):
        self.name = name
        self.artist_id = artist_id


class RemixSchema(Schema):
    name = fields.String(description="The name of the remix")
    artist_id = fields.String(description="The ID of the artist", data_key="artistId")

    @post_load
    def create_remix(self, data, **kwargs):
        return Remix(**data)

    class Meta:
        unknown = EXCLUDE


class Track:
    def __init__(self, name, artist_id, remix, id=None):
        self.id = id
        self.artist_id = artist_id
        self.name = name
        self.remix = remix


class TrackSchema(Schema):
    id = fields.String(description="The ID of the track")
    name = fields.String(description="The name of the track")
    artist_id = fields.String(description="The ID of the artist", data_key="artistId")
    remix = fields.Nested(RemixSchema, allow_none=True)

    @post_load
    def create_track(self, data, **kwargs):
        return Track(**data)

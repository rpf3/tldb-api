from marshmallow import Schema, fields, post_load


class Artist:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name


class ArtistSchema(Schema):
    id = fields.String(description="The ID of the artist")
    name = fields.String(description="The name of the artist")

    @post_load
    def create_artist(self, data, **kwargs):
        return Artist(**data)


class WriteArtistSchema(ArtistSchema):
    class Meta:
        exclude = ["id"]

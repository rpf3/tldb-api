from marshmallow import EXCLUDE, fields, post_load

from tldb.models.schema import BaseSchema


class Artist:
    def __init__(self, name=None, id=None):
        self.id = id
        self.name = name


class ArtistSchema(BaseSchema):
    id = fields.String(description="The ID of the artist")
    name = fields.String(description="The name of the artist")

    @post_load
    def create_artist(self, data, **kwargs):
        return Artist(**data)


class ArtistWriteSchema(ArtistSchema):
    class Meta:
        exclude = ["id"]
        unknown = EXCLUDE


class ArtistIdSchema(ArtistSchema):
    class Meta:
        fields = ["id"]

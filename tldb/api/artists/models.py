from flask_smorest import Blueprint
from marshmallow import Schema, fields

blp = Blueprint("artists", "artists", url_prefix="/artists")


class CreateArtistSchema(Schema):
    name = fields.String(description="The name of the artist")


class GetArtistSchema(CreateArtistSchema):
    id = fields.String(description="The ID of the artist", dump_only=True)


class UpdateArtistSchema(CreateArtistSchema):
    id = fields.String(description="The ID of the artist")

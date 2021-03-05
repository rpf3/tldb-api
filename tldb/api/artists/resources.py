from flask_restx import Resource, marshal

from tldb.api.artists import models
from tldb.api.artists.models import api
from tldb.database.artist import Artist as ArtistTable


@api.route("")
class Artists(Resource):
    def __init__(self, res):
        super().__init__(res)

        self.table = ArtistTable()

    def get(self):
        """
        List all artists
        """
        database_response = self.table.get()

        return list(database_response)

    @api.expect(models.artist)
    def post(self):
        """
        Create a new artist
        """
        api_model = marshal(api.payload, models.artist)

        del api_model["id"]

        database_response = self.table.insert(api_model)
        artist_id = database_response[0]

        return artist_id

    @api.expect(models.artists)
    def patch(self):
        """
        Create or update a set of artists
        """
        api_model = marshal(api.payload, models.artists)

        database_response = self.table.upsert(api_model.get("artists"))

        return database_response


@api.route("/<string:id>")
class Artist(Resource):
    def __init__(self, res):
        super().__init__(res)

        self.table = ArtistTable()

    def get(self, id):
        """
        Get a single artist
        """
        database_response = self.table.get(id)

        return database_response

    @api.expect(models.artist)
    def put(self, id):
        """
        Update a single artist
        """
        api_model = marshal(api.payload, models.artist)

        api_model["id"] = id

        database_response = self.table.update([api_model])

        return list(database_response)
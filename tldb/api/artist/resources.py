from flask_restx import Resource, marshal

from tldb.api.artist import models
from tldb.api.artist.models import api
from tldb.database import tables


@api.route("")
class Artists(Resource):
    def get(self):
        """
        List all artists
        """
        artist_table = tables.Artist()

        database_response = artist_table.get()

        return list(database_response)

    @api.expect(models.artist)
    def post(self):
        """
        Create a new artist
        """
        artist_table = tables.Artist()

        api_model = marshal(api.payload, models.artist)

        del api_model["id"]

        database_response = artist_table.insert(api_model)
        artist_id = database_response[0]

        return artist_id

    @api.expect(models.artists)
    def patch(self):
        """
        Create or update a set of artists
        """
        artist_table = tables.Artist()

        api_model = marshal(api.payload, models.artists)

        insert_models = []
        update_models = []

        for artist in api_model.get("artists"):
            if artist["id"] is None:
                del artist["id"]

                insert_models.append(artist)
            else:
                update_models.append(artist)

        new_artist_ids = artist_table.insert(insert_models)
        update_artist_ids = artist_table.update(update_models)

        artist_ids = new_artist_ids + update_artist_ids

        return artist_ids


@api.route("/<string:id>")
class Artist(Resource):
    def get(self, id):
        """
        Get a single artist
        """
        artist_table = tables.Artist()

        database_response = artist_table.get(id)

        return database_response

    @api.expect(models.artist)
    def put(self, id):
        """
        Update a single artist
        """
        artist_table = tables.Artist()

        api_model = marshal(api.payload, models.artist)

        api_model["id"] = id

        database_response = artist_table.update([api_model])

        return database_response

from flask_restx import abort
from rethinkdb import r

from tldb.database import utils
from tldb.database.connection import DATABASE_NAME, Connection

TABLE_NAME = "artist"
DEFAULT_LIMIT = 10


class Artist:
    def __init__(self):
        self.table = r.db(DATABASE_NAME).table(TABLE_NAME)

    def get(self, id=None):
        if id is None:
            query = self.table.limit(DEFAULT_LIMIT)
        else:
            query = self.table.get(id)

        with Connection() as conn:
            result = conn.run(query)

        return result

    def get_all(self, ids):
        query = self.table.get_all(*ids)

        with Connection() as conn:
            result = conn.run(query)

        return list(result)

    def search_name(self, name):
        query = self.table.get_all(name.lower(), index="name")

        with Connection() as conn:
            result = conn.run(query)

        return list(result)

    def insert(self, artists):
        if len(artists) > 0:
            query = self.table.insert(artists)

            with Connection() as conn:
                result = conn.run(query)

            artist_ids = result["generated_keys"]
        else:
            artist_ids = []

        return self.get_all(artist_ids)

    def update(self, artists):
        if len(artists) > 0:
            self.validate(artists)

            query = self.table.insert(artists, conflict="update")

            with Connection() as conn:
                conn.run(query)

            artist_ids = utils.get_ids(artists)
        else:
            artist_ids = []

        return self.get_all(artist_ids)

    def upsert(self, artists):
        new_artists = []
        existing_artists = []

        for artist in artists:
            if artist.get("id") is not None:
                existing_artists.append(artist)
            else:
                if "id" in artist:
                    del artist["id"]

                new_artists.append(artist)

        result = self.insert(new_artists) + self.update(existing_artists)

        return result

    def validate(self, artists):
        artist_ids = utils.get_ids(artists)

        query = self.table.get_all(*artist_ids).pluck("id")

        with Connection() as conn:
            result = conn.run(query)

        result_ids = utils.get_ids(result)

        invalid_ids = []

        for id in artist_ids:
            if id not in result_ids:
                invalid_ids.append(id)

        if len(invalid_ids) > 0:
            abort(400, "Invalid artist IDs", ids=invalid_ids)


def get_artist(obj):
    result = {"artist": r.db(DATABASE_NAME).table(TABLE_NAME).get(obj["artistId"])}

    return result

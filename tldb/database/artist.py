from flask_smorest import abort
from rethinkdb import r

from tldb.database.connection import DATABASE_NAME, Connection
from tldb.models import ArtistSchema, ArtistWriteSchema

TABLE_NAME = "artist"
DEFAULT_LIMIT = 10


class ArtistTable:
    def __init__(self):
        self.table = r.db(DATABASE_NAME).table(TABLE_NAME)

    def get(self, id=None):
        if id is None:
            query = self.table.limit(DEFAULT_LIMIT)
        else:
            query = self.table.get_all(id)

        with Connection() as conn:
            result = conn.run(query)

        schema = ArtistSchema(many=True)
        artists = schema.load(result)

        return artists

    def get_all(self, ids):
        query = self.table.get_all(*ids)

        with Connection() as conn:
            result = conn.run(query)

        schema = ArtistSchema(many=True)
        artists = schema.load(result)

        return artists

    def search_name(self, name):
        query = self.table.get_all(name.lower(), index="name")

        with Connection() as conn:
            result = conn.run(query)

        return list(result)

    def insert(self, artists):
        if len(artists) > 0:
            schema = ArtistWriteSchema(many=True)
            json_data = schema.dump(artists)
            query = self.table.insert(json_data)

            with Connection() as conn:
                result = conn.run(query)

            artist_ids = result["generated_keys"]
        else:
            artist_ids = []

        return self.get_all(artist_ids)

    def update(self, artists):
        if len(artists) > 0:
            artist_ids = {x.id for x in artists}

            self.validate(artist_ids)

            schema = ArtistSchema(many=True)
            json_data = schema.dump(artists)

            query = self.table.insert(json_data, conflict="update")

            with Connection() as conn:
                conn.run(query)
        else:
            artist_ids = []

        return self.get_all(artist_ids)

    def upsert(self, artists):
        new_artists = []
        existing_artists = []

        for artist in artists:
            if artist.id is not None:
                existing_artists.append(artist)
            else:
                new_artists.append(artist)

        result = self.insert(new_artists) + self.update(existing_artists)

        return result

    def validate(self, artist_ids):
        query = self.table.get_all(*artist_ids).pluck("id")

        with Connection() as conn:
            result = conn.run(query)

        result_ids = {x.get("id") for x in result}

        invalid_ids = []

        for id in artist_ids:
            if id not in result_ids:
                invalid_ids.append(id)

        if len(invalid_ids) > 0:
            abort(400, message="Invalid artist IDs")


def get_artist(obj):
    result = {"artist": r.db(DATABASE_NAME).table(TABLE_NAME).get(obj["artist"]["id"])}

    return result


def get_artists(obj):
    result = {
        "artists": obj["artists"].merge(
            lambda artist: r.db(DATABASE_NAME).table(TABLE_NAME).get(artist["id"])
        )
    }

    return result

from flask_smorest import abort
from rethinkdb import r

from tldb.database.connection import DATABASE_NAME, Connection
from tldb.models import ArtistSchema, ArtistWriteSchema

TABLE_NAME = "artist"
DEFAULT_LIMIT = 10


class Table:
    def __init__(self):
        self.table = r.db(DATABASE_NAME).table(TABLE_NAME)

    def get(self, ids):
        db_query = self.table.get_all(*ids)

        with Connection() as conn:
            result = conn.run(db_query)

        schema = ArtistSchema(many=True)
        artists = schema.load(result)

        return artists

    def insert(self, artists):
        if len(artists) > 0:
            schema = ArtistWriteSchema(many=True)
            json_data = schema.dump(artists)
            db_query = self.table.insert(json_data)

            with Connection() as conn:
                result = conn.run(db_query)

            artist_ids = result["generated_keys"]
        else:
            artist_ids = []

        return self.get(artist_ids)

    def update(self, artists):
        if len(artists) > 0:
            artist_ids = {x.id for x in artists}

            self._validate(artist_ids)

            schema = ArtistSchema(many=True)
            json_data = schema.dump(artists)

            db_query = self.table.insert(json_data, conflict="update")

            with Connection() as conn:
                conn.run(db_query)
        else:
            artist_ids = []

        return self.get(artist_ids)

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

    def search(self, query, params):
        search_string = (query or "").strip().lower()

        if search_string == "":
            db_query = self.table
        else:
            db_query = self.table.get_all(search_string, index="name")

        db_query = db_query.skip(params.skip).limit(params.take)

        with Connection() as conn:
            result = conn.run(db_query)

        schema = ArtistSchema(many=True)
        artists = schema.load(result)

        return artists

    def _validate(self, ids):
        db_query = self.table.get_all(*ids).pluck("id")

        with Connection() as conn:
            result = conn.run(db_query)

        result_ids = {x.get("id") for x in result}

        invalid_ids = []

        for id in ids:
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

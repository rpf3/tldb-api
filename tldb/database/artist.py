from flask_restx import abort
from rethinkdb import r

from tldb.database import utils
from tldb.database.connection import DATABASE_NAME, Connection

TABLE_NAME = "artist"


class Artist:
    def __init__(self):
        self.table = r.db(DATABASE_NAME).table(TABLE_NAME)

    def get(self, id=None):
        with Connection() as conn:
            if id is None:
                result = conn.run(self.table)
            else:
                result = conn.run(self.table.get(id))

        return result

    def insert(self, artists):
        if len(artists) > 0:
            with Connection() as conn:
                query = self.table.insert(artists)

                result = conn.run(query)

            artist_ids = result["generated_keys"]
        else:
            artist_ids = []

        return artist_ids

    def update(self, artists):
        if len(artists) > 0:
            self.validate(artists)

            with Connection() as conn:
                query = self.table.insert(artists, conflict="update")

                conn.run(query)

            artist_ids = list(utils.get_ids(artists))
        else:
            artist_ids = []

        return artist_ids

    def validate(self, artists):
        artist_ids = utils.get_ids(artists)

        with Connection() as conn:
            query = self.table.get_all(*artist_ids).pluck("id")

            result = conn.run(query)

        result_ids = utils.get_ids(result)

        invalid_ids = []

        for id in artist_ids:
            if id not in result_ids:
                invalid_ids.append(id)

        if len(invalid_ids) > 0:
            abort(400, "Invalid artist IDs", ids=invalid_ids)

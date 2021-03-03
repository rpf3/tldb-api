import os

from flask_restx import abort
from rethinkdb import r

from tldb.database import utils

DATABASE_NAME = "tldb"


class Connection:
    def __init__(self):
        self._host = os.environ["RETHINKDB_HOST"]
        self._port = os.environ["RETHINKDB_PORT"]

    def __enter__(self):
        self._conn = r.connect(host=self._host, port=self._port)

        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if self._conn is not None:
            self._conn.close()

    def run(self, query):
        result = query.run(self._conn)

        return result


class Artist:
    _table_name = "artist"

    def __init__(self):
        self.table = r.db(DATABASE_NAME).table(self._table_name)

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

            artist_ids = utils.get_ids(artists)
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


class Track:
    _table_name = "track"

    def __init__(self):
        self.table = r.db(DATABASE_NAME).table(self._table_name)

    def get(self, id=None):
        with Connection() as conn:
            if id is None:
                result = conn.run(self.table)
            else:
                result = conn.run(self.table.get(id))

        return result

    def insert(self, tracks):
        if len(tracks) > 0:
            with Connection() as conn:
                query = self.table.insert(tracks)

                result = conn.run(query)

            track_ids = result["generated_keys"]
        else:
            track_ids = []

        return track_ids

    def update(self, tracks):
        if len(tracks) > 0:
            self.validate(tracks)

            with Connection() as conn:
                query = self.table.insert(tracks, conflict="update")

                conn.run(query)

            track_ids = utils.get_ids(tracks)
        else:
            track_ids = []

        return track_ids

    def validate(self, tracks):
        track_ids = utils.get_ids(tracks)

        with Connection() as conn:
            query = self.table.get_all(*track_ids).pluck("id")

            result = conn.run(query)

        result_ids = utils.get_ids(result)

        invalid_ids = []

        for id in track_ids:
            if id not in result_ids:
                invalid_ids.append(id)

        if len(invalid_ids) > 0:
            abort(400, "Invalid track IDs", ids=invalid_ids)


class Tracklist:
    _table_name = "tracklist"

    def __init__(self):
        self.table = r.db(DATABASE_NAME).table(self._table_name)

    def get(self, id=None):
        with Connection() as conn:
            if id is None:
                result = conn.run(self.table)
            else:
                result = conn.run(self.table.get(id))

        return result

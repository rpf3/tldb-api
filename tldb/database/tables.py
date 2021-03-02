import os

from rethinkdb import r

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
        with Connection() as conn:
            query = self.table.insert(artists, conflict="update")

            conn.run(query)

        artist_ids = [artist.get("id") for artist in artists]

        return artist_ids


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

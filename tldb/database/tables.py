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

    def get(self, id=None):
        with Connection() as conn:
            table_query = r.db(DATABASE_NAME).table(self._table_name)

            if id is None:
                result = conn.run(table_query)
            else:
                result = conn.run(table_query.get(id))

        return result


class Track:
    _table_name = "track"

    def get(self, id=None):
        with Connection() as conn:
            table_query = r.db(DATABASE_NAME).table(self._table_name)

            if id is None:
                result = conn.run(table_query)
            else:
                result = conn.run(table_query.get(id))

        return result


class Tracklist:
    _table_name = "tracklist"

    def get(self, id=None):
        with Connection() as conn:
            table_query = r.db(DATABASE_NAME).table(self._table_name)

            if id is None:
                result = conn.run(table_query)
            else:
                result = conn.run(table_query.get(id))

        return result

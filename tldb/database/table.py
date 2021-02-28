import os

from rethinkdb import r


class Connection:
    _database_name = "tldb"

    def __init__(self):
        self._host = os.environ["RETHINKDB_HOST"]
        self._port = os.environ["RETHINKDB_PORT"]

    def __enter__(self):
        self._conn = r.connect(host=self._host, port=self._port)

        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if self._conn is not None:
            self._conn.close()


class Artist(Connection):
    _table_name = "artist"

from rethinkdb import r

from tldb.database.connection import DATABASE_NAME, Connection


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

from rethinkdb import r

from tldb.database.connection import DATABASE_NAME, Connection

TABLE_NAME = "tracklist"


class Tracklist:
    def __init__(self):
        self.table = r.db(DATABASE_NAME).table(TABLE_NAME)

    def get(self, id=None):
        with Connection() as conn:
            if id is None:
                result = conn.run(self.table)
            else:
                result = conn.run(self.table.get(id))

        return result

from rethinkdb import r

from tldb.database.connection import DATABASE_NAME, Connection

TABLE_NAME = "tracklist"


class Tracklist:
    def __init__(self):
        self.table = r.db(DATABASE_NAME).table(TABLE_NAME)

    def get(self, id=None):
        if id is None:
            query = self.table
        else:
            query = self.table.get(id)

        with Connection() as conn:
            result = conn.run(query)

        return result

from rethinkdb import r

from tldb.database import utils
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

    def get_all(self, ids):
        query = self.table.get_all(*ids)

        with Connection() as conn:
            result = conn.run(query)

        return list(result)

    def insert(self, tracklists):
        if len(tracklists) > 0:
            query = self.table.insert(tracklists)

            with Connection() as conn:
                result = conn.run(query)

            tracklist_ids = result["generated_keys"]
        else:
            tracklist_ids = []

        return self.get_all(tracklist_ids)

    def update(self, tracklists):
        if len(tracklists) > 0:
            query = self.table.insert(tracklists, conflict="update")

            with Connection() as conn:
                conn.run(query)

            tracklist_ids = utils.get_ids(tracklists)
        else:
            tracklist_ids = []

        return self.get_all(tracklist_ids)

from flask_restx import abort
from rethinkdb import r

from tldb.database import artist, utils
from tldb.database.connection import DATABASE_NAME, Connection

TABLE_NAME = "tracklist"


class Tracklist:
    def __init__(self):
        self.table = r.db(DATABASE_NAME).table(TABLE_NAME)

    def get(self, id=None, verbose=False):
        if id is None:
            query = self.table
        else:
            query = self.table.get(id)

        if verbose is True:
            final_query = query.merge(
                lambda tracklist: {
                    "artist": r.db(DATABASE_NAME)
                    .table(artist.TABLE_NAME)
                    .get(tracklist["artistId"])
                }
            )
        else:
            final_query = query

        with Connection() as conn:
            result = conn.run(final_query)

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
            self.validate(tracklists)

            query = self.table.insert(tracklists, conflict="update")

            with Connection() as conn:
                conn.run(query)

            tracklist_ids = utils.get_ids(tracklists)
        else:
            tracklist_ids = []

        return self.get_all(tracklist_ids)

    def validate(self, tracklists):
        tracklist_ids = utils.get_ids(tracklists)

        query = self.table.get_all(*tracklist_ids).pluck("id")

        with Connection() as conn:
            result = conn.run(query)

        result_ids = utils.get_ids(result)

        invalid_ids = []

        for id in tracklist_ids:
            if id not in result_ids:
                invalid_ids.append(id)

        if len(invalid_ids) > 0:
            abort(400, "Invalid tracklist IDs", ids=invalid_ids)

from flask_restx import abort
from rethinkdb import r

from tldb.database import utils
from tldb.database.connection import DATABASE_NAME, Connection


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

            track_ids = list(utils.get_ids(tracks))
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

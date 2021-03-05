from flask_restx import abort
from rethinkdb import r

from tldb.database import artist, utils
from tldb.database.connection import DATABASE_NAME, Connection

TABLE_NAME = "track"
DEFAULT_LIMIT = 10


class Track:
    def __init__(self):
        self.table = r.db(DATABASE_NAME).table(TABLE_NAME)

    def get(self, id=None, verbose=False):
        if id is None:
            track_query = self.table.limit(DEFAULT_LIMIT)
        else:
            track_query = self.table.get(id)

        if verbose is True:
            final_query = track_query.merge(
                lambda track: {
                    "artist": r.db(DATABASE_NAME)
                    .table(artist.TABLE_NAME)
                    .get(track["artistId"])
                }
            )
        else:
            final_query = track_query

        with Connection() as conn:
            result = conn.run(final_query)

        return result

    def get_all(self, ids):
        query = self.table.get_all(*ids)

        with Connection() as conn:
            result = conn.run(query)

        return list(result)

    def insert(self, tracks):
        if len(tracks) > 0:
            query = self.table.insert(tracks)

            with Connection() as conn:
                result = conn.run(query)

            track_ids = result["generated_keys"]
        else:
            track_ids = []

        return self.get_all(track_ids)

    def update(self, tracks):
        if len(tracks) > 0:
            self.validate(tracks)

            query = self.table.insert(tracks, conflict="update")

            with Connection() as conn:
                conn.run(query)

            track_ids = utils.get_ids(tracks)
        else:
            track_ids = []

        return self.get_all(track_ids)

    def upsert(self, tracks):
        new_tracks = []
        existing_tracks = []

        for track in tracks:
            if track.get("id") is not None:
                existing_tracks.append(track)
            else:
                if "id" in track:
                    del track["id"]

                new_tracks.append(track)

        result = self.insert(new_tracks) + self.update(existing_tracks)

        return result

    def validate(self, tracks):
        track_ids = utils.get_ids(tracks)

        query = self.table.get_all(*track_ids).pluck("id")

        with Connection() as conn:
            result = conn.run(query)

        result_ids = utils.get_ids(result)

        invalid_ids = []

        for id in track_ids:
            if id not in result_ids:
                invalid_ids.append(id)

        if len(invalid_ids) > 0:
            abort(400, "Invalid track IDs", ids=invalid_ids)

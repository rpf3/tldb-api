from flask_smorest import abort
from rethinkdb import r

from tldb.database.artist import get_artist, get_artists
from tldb.database.connection import DATABASE_NAME, Connection
from tldb.database.track import TABLE_NAME as TRACK_TABLE_NAME
from tldb.database.track import get_remix
from tldb.models import TracklistSchema, WriteTracklistSchema

TABLE_NAME = "tracklist"
DEFAULT_LIMIT = 10
DEFAULT_SORT_INDEX = "date"


class TracklistTable:
    def __init__(self):
        self.table = r.db(DATABASE_NAME).table(TABLE_NAME)

    def get(self, id=None, skip=0, take=DEFAULT_LIMIT, verbose=False):
        if id is None:
            query = self.table.skip(skip).limit(take)
        else:
            query = self.table.get_all(id)

        if verbose is True:
            final_query = query.merge(get_artists).merge(
                lambda tracklist: {
                    "tracks": r.expr(tracklist["tracks"]).merge(
                        lambda track: {
                            "track": r.db(DATABASE_NAME)
                            .table(TRACK_TABLE_NAME)
                            .get(track["id"])
                            .merge(get_artist)
                            .merge(get_remix)
                        }
                    )
                }
            )
        else:
            final_query = query

        with Connection() as conn:
            result = conn.run(final_query)

        schema = TracklistSchema(many=True)
        tracklists = schema.load(result)

        return tracklists

    def get_all(self, ids):
        query = self.table.get_all(*ids)

        with Connection() as conn:
            result = conn.run(query)

        schema = TracklistSchema(many=True)
        tracklists = schema.load(result)

        return tracklists

    def insert(self, tracklists):
        if len(tracklists) > 0:
            schema = WriteTracklistSchema(many=True)
            json_data = schema.dump(tracklists)
            query = self.table.insert(json_data)

            with Connection() as conn:
                result = conn.run(query)

            tracklist_ids = result["generated_keys"]
        else:
            tracklist_ids = []

        return self.get_all(tracklist_ids)

    def update(self, tracklists):
        if len(tracklists) > 0:
            tracklist_ids = {x.id for x in tracklists}

            self.validate(tracklist_ids)

            schema = TracklistSchema(many=True)
            json_data = schema.dump(tracklists)

            query = self.table.insert(json_data, conflict="update")

            with Connection() as conn:
                conn.run(query)
        else:
            tracklist_ids = []

        return self.get_all(tracklist_ids)

    def upsert(self, tracklists):
        new_tracklists = []
        existing_tracklists = []

        for tracklist in tracklists:
            if tracklist.id is not None:
                existing_tracklists.append(tracklist)
            else:
                new_tracklists.append(tracklist)

        result = self.insert(new_tracklists) + self.update(existing_tracklists)

        return result

    def validate(self, tracklist_ids):
        query = self.table.get_all(*tracklist_ids).pluck("id")

        with Connection() as conn:
            result = conn.run(query)

        result_ids = {x.get("id") for x in result}

        invalid_ids = []

        for id in tracklist_ids:
            if id not in result_ids:
                invalid_ids.append(id)

        if len(invalid_ids) > 0:
            abort(400, message="Invalid tracklist IDs")

from flask_smorest import abort
from rethinkdb import r

from tldb.database.artist import get_artist, get_artists
from tldb.database.connection import DATABASE_NAME, Connection
from tldb.database.track import TABLE_NAME as TRACK_TABLE_NAME
from tldb.database.track import get_remix
from tldb.models import TracklistSchema, TracklistWriteSchema

TABLE_NAME = "tracklist"
DEFAULT_SORT_INDEX = "date"


class Table:
    def __init__(self):
        self.table = r.db(DATABASE_NAME).table(TABLE_NAME)

    def get(self, ids, verbose):
        db_query = self.table.get_all(*ids)

        if verbose is True:
            db_query = self._create_verbose_query(db_query)

        with Connection() as conn:
            result = conn.run(db_query)

        schema = TracklistSchema(many=True)
        tracklists = schema.load(result)

        return tracklists

    def insert(self, tracklists):
        if len(tracklists) > 0:
            schema = TracklistWriteSchema(many=True)
            json_data = schema.dump(tracklists)
            db_query = self.table.insert(json_data)

            with Connection() as conn:
                result = conn.run(db_query)

            tracklist_ids = result["generated_keys"]
        else:
            tracklist_ids = []

        return self.get(tracklist_ids, False)

    def update(self, tracklists):
        if len(tracklists) > 0:
            tracklist_ids = {x.id for x in tracklists}

            self._validate(tracklist_ids)

            schema = TracklistSchema(many=True)
            json_data = schema.dump(tracklists)

            db_query = self.table.insert(json_data, conflict="update")

            with Connection() as conn:
                conn.run(db_query)
        else:
            tracklist_ids = []

        return self.get(tracklist_ids, False)

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

    def search(self, query, skip, take, verbose):
        search_string = (query or "").strip()

        def filter_query(tracklist):
            if search_string == "":
                result = True
            else:
                result = tracklist["name"].match(f"(?i).*{search_string}.*")

            return result

        db_query = (
            self.table.order_by(index=r.desc(DEFAULT_SORT_INDEX))
            .filter(filter_query)
            .skip(skip)
            .limit(take)
        )

        if verbose is True:
            db_query = self._create_verbose_query(db_query)

        with Connection() as conn:
            result = conn.run(db_query)

        schema = TracklistSchema(many=True)
        tracklists = schema.load(result)

        return tracklists

    def _validate(self, ids):
        db_query = self.table.get_all(*ids).pluck("id")

        with Connection() as conn:
            result = conn.run(db_query)

        result_ids = {x.get("id") for x in result}

        invalid_ids = []

        for id in ids:
            if id not in result_ids:
                invalid_ids.append(id)

        if len(invalid_ids) > 0:
            abort(400, message="Invalid tracklist IDs")

    def _create_verbose_query(self, db_query):
        verbose_query = db_query.merge(get_artists).merge(
            lambda tracklist: {
                "tracks": r.expr(tracklist["tracks"]).merge(
                    lambda track: {
                        "track": r.db(DATABASE_NAME)
                        .table(TRACK_TABLE_NAME)
                        .get(track["track"]["id"])
                        .merge(get_artist)
                        .merge(get_remix)
                    }
                )
            }
        )

        return verbose_query

    def get_all_by_artist(self, artist_id, skip, take):
        db_query = (
            self.table.filter(
                lambda tracklist: tracklist["artists"]
                .map(lambda artist: artist["id"])
                .contains(artist_id)
            )
            .skip(skip)
            .limit(take)
        )

        with Connection() as conn:
            result = conn.run(db_query)

        schema = TracklistSchema(many=True)
        tracklists = schema.load(result)

        return tracklists

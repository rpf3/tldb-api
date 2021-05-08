from flask_smorest import abort
from rethinkdb import r

from tldb.database.artist import get_artist
from tldb.database.connection import DATABASE_NAME, Connection
from tldb.models import TrackSchema, TrackWriteSchema

TABLE_NAME = "track"


class Table:
    def __init__(self):
        self.table = r.db(DATABASE_NAME).table(TABLE_NAME)

    def get(self, ids, verbose):
        db_query = self.table.get_all(*ids)

        if verbose is True:
            db_query = self._create_verbose_query(db_query)

        with Connection() as conn:
            result = conn.run(db_query)

        schema = TrackSchema(many=True)
        tracks = schema.load(result)

        return tracks

    def insert(self, tracks):
        if len(tracks) > 0:
            schema = TrackWriteSchema(many=True)
            json_data = schema.dump(tracks)
            db_query = self.table.insert(json_data)

            with Connection() as conn:
                result = conn.run(db_query)

            track_ids = result["generated_keys"]
        else:
            track_ids = []

        return self.get(track_ids, False)

    def update(self, tracks):
        if len(tracks) > 0:
            track_ids = {x.id for x in tracks}

            self._validate(track_ids)

            schema = TrackSchema(many=True)
            json_data = schema.dump(tracks)

            db_query = self.table.insert(json_data, conflict="update")

            with Connection() as conn:
                conn.run(db_query)
        else:
            track_ids = []

        return self.get(track_ids, False)

    def upsert(self, tracks):
        new_tracks = []
        existing_tracks = []

        for track in tracks:
            if track.id is not None:
                existing_tracks.append(track)
            else:
                new_tracks.append(track)

        result = self.insert(new_tracks) + self.update(existing_tracks)

        return result

    def search(self, query, params):
        search_string = (query or "").strip().lower()

        def filter_query(track):
            if search_string == "":
                result = True
            else:
                result = track["name"].match(f"(?i).*{search_string}.*")

            return result

        if search_string == "":
            db_query = self.table
        elif params.exact:
            db_query = self.table.get_all(search_string, index="name")
        else:
            db_query = self.table.filter(filter_query)

        db_query = db_query.skip(params.skip).limit(params.take)

        if params.verbose is True:
            db_query = self._create_verbose_query(db_query)

        with Connection() as conn:
            result = conn.run(db_query)

        schema = TrackSchema(many=True)
        tracks = schema.load(result)

        return tracks

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
            abort(400, message="Invalid track IDs")

    def _create_verbose_query(self, db_query):
        verbose_query = db_query.merge(get_artist).merge(get_remix)

        return verbose_query

    def get_all_by_artist(self, artist_id, params):
        def filter_query(track):
            return track["artist"]["id"].eq(artist_id)

        db_query = self.table.filter(filter_query).skip(params.skip).limit(params.take)

        if params.verbose is True:
            db_query = self._create_verbose_query(db_query)

        with Connection() as conn:
            result = conn.run(db_query)

        schema = TrackSchema(many=True)
        tracks = schema.load(result)

        return tracks

    def get_exact_match(self, name, artistId, remix_name, remix_artist_id):
        db_query = self.table.get_all(name.lower(), index="name").filter(
            r.row["artist"]["id"].eq(artistId)
        )

        if remix_artist_id is not None:
            db_query = db_query.filter(
                lambda track: track["remix"]["artist"]["id"].eq(remix_artist_id)
                and track["remix"]["name"].eq(remix_name)
            )

        with Connection() as conn:
            result = conn.run(db_query)

        schema = TrackSchema(many=True)
        tracks = schema.load(result)

        if len(tracks) > 0:
            track = tracks[0]
        else:
            track = None

        return track


def get_remix(obj):
    result = {
        "remix": r.branch(obj.has_fields("remix"), get_artist(obj["remix"]), None)
    }

    return result

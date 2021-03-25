from flask_smorest import abort
from rethinkdb import r

from tldb.database.artist import get_artist
from tldb.database.connection import DATABASE_NAME, Connection
from tldb.models import TrackSchema

TABLE_NAME = "track"
DEFAULT_LIMIT = 10


class Track:
    def __init__(self):
        self.table = r.db(DATABASE_NAME).table(TABLE_NAME)

    def get(self, id=None, verbose=False):
        if id is None:
            track_query = self.table.limit(DEFAULT_LIMIT)
        else:
            track_query = self.table.get_all(id)

        if verbose is True:
            final_query = (
                track_query.merge(get_artist)
                .merge(get_remix)
                .merge(
                    lambda track: {
                        "versions": r.branch(
                            track.has_fields("versions"),
                            r.db(DATABASE_NAME)
                            .table(TABLE_NAME)
                            .get_all(r.args(track["versions"]))
                            .merge(get_artist)
                            .merge(get_remix)
                            .coerce_to("array"),
                            [],
                        )
                    }
                )
            )
        else:
            final_query = track_query

        with Connection() as conn:
            result = conn.run(final_query)

        schema = TrackSchema(many=True)
        tracks = schema.load(result)

        return tracks

    def get_all(self, ids):
        query = self.table.get_all(*ids)

        with Connection() as conn:
            result = conn.run(query)

        schema = TrackSchema(many=True)
        tracks = schema.load(result)

        return tracks

    def get_exact_match(self, name, artistId, remix_name=None, remix_artist_id=None):
        query = self.table.get_all(name.lower(), index="name").filter(
            r.row["artistId"].eq(artistId)
        )

        if remix_artist_id is not None:
            query = query.filter(
                lambda track: track["remix"]["artistId"].eq(remix_artist_id)
                and track["remix"]["name"].eq(remix_name)
            )

        with Connection() as conn:
            cursor = conn.run(query)

        results = list(cursor)

        if len(results) > 0:
            result = results[0]
        else:
            result = None

        return result

    def get_versions_by_original(self, ids):
        query = self.table.get_all(*ids, index="originalId")

        with Connection() as conn:
            cursor = conn.run(query)

        result = list(cursor)

        return result

    def search_name(self, name):
        query = self.table.get_all(name.lower(), index="name")

        with Connection() as conn:
            result = conn.run(query)

        return list(result)

    def insert(self, tracks):
        if len(tracks) > 0:
            schema = TrackSchema(many=True, exclude=["id"])
            json_data = schema.dump(tracks)
            query = self.table.insert(json_data)

            with Connection() as conn:
                result = conn.run(query)

            track_ids = result["generated_keys"]
        else:
            track_ids = []

        return self.get_all(track_ids)

    def update(self, tracks):
        if len(tracks) > 0:
            track_ids = {x.id for x in tracks}

            self.validate(track_ids)

            schema = TrackSchema(many=True)
            json_data = schema.dump(tracks)

            query = self.table.insert(json_data, conflict="update")

            with Connection() as conn:
                conn.run(query)
        else:
            track_ids = []

        return self.get_all(track_ids)

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

    def validate(self, track_ids):
        query = self.table.get_all(*track_ids).pluck("id")

        with Connection() as conn:
            result = conn.run(query)

        result_ids = {x.get("id") for x in result}

        invalid_ids = []

        for id in track_ids:
            if id not in result_ids:
                invalid_ids.append(id)

        if len(invalid_ids) > 0:
            abort(400, message="Invalid track IDs")


def get_remix(obj):
    result = {
        "remix": r.branch(obj["remix"].eq(None), obj["remix"], get_artist(obj["remix"]))
    }

    return result

import os

from rethinkdb import r

DATABASE_NAME = "tldb"


def create_database(conn):
    if r.db_list().contains(DATABASE_NAME).run(conn):
        r.db_drop(DATABASE_NAME).run(conn)

    r.db_create(DATABASE_NAME).run(conn)


def create_artist_table(conn):
    r.db(DATABASE_NAME).table_create("artist").run(conn)


def create_track_table(conn):
    r.db(DATABASE_NAME).table_create("track").run(conn)


def create_tracklist_table(conn):
    r.db(DATABASE_NAME).table_create("tracklist").run(conn)

    # Create a secondary index on the date
    r.db(DATABASE_NAME).table("tracklist").index_create("date").run(conn)


if __name__ == "__main__":
    host = os.environ["RETHINKDB_HOST"]
    port = os.environ["RETHINKDB_PORT"]

    try:
        conn = r.connect(host=host, port=port)

        create_database(conn)
        create_artist_table(conn)
        create_track_table(conn)
        create_tracklist_table(conn)
    finally:
        conn.close()

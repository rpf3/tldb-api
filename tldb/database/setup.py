from rethinkdb import r

from tldb.database.table import Artist, Connection


def create_database():
    with Connection() as conn:
        if r.db_list().contains(conn._database_name).run(conn._conn):
            r.db_drop(conn._database_name).run(conn._conn)

        r.db_create(conn._database_name).run(conn._conn)


def create_artist_table():
    with Artist() as artist:
        r.db(artist._database_name).table_create(artist._table_name).run(artist._conn)


def create():
    create_database()
    create_artist_table()

from rethinkdb import r

from tldb.database import table
from tldb.database.table import Artist, Connection


def create_database():
    try:
        with Connection() as conn:
            if conn.run(r.db_list().contains(table.DATABASE_NAME)):
                conn.run(r.db_drop(table.DATABASE_NAME))

            conn.run(r.db_create(table.DATABASE_NAME))
    except Exception as e:
        print(e)


def create_artist_table():
    with Connection() as conn:
        conn.run(r.db(table.DATABASE_NAME).table_create(Artist._table_name))


def create():
    create_database()
    create_artist_table()

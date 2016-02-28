"""Database provisioning."""
import psycopg2.extras
import sys
import urlparse


def setup(new_conn, cursor):
    """Bootstrap the database.

    Assumes no existing database.
    """
    print 'Setting up hstore...'
    cursor.execute("""CREATE EXTENSION hstore;""")

    print 'Setting up jsonb...'
    psycopg2.extras.register_json(new_conn, name='jsonb')

    print 'Creating "report" table...'
    cursor.execute("""
        CREATE TABLE report
            (
                domain varchar PRIMARY KEY,
                data jsonb,
                generated timestamp
            );
    """)

    print 'Creating "delta" table...'
    cursor.execute("""
        CREATE TABLE delta
            (
                domain varchar PRIMARY KEY,
                deltas jsonb,
                generated timestamp
            );
    """)


if __name__ == '__main__':

    db_url = sys.argv[-1]
    if not db_url.startswith('postgres'):
        raise Exception('Missing database url')

    urlparse.uses_netloc.append("postgres")
    new_url = urlparse.urlparse(db_url)

    new_conn = psycopg2.connect(
        database=new_url.path[1:],
        user=new_url.username,
        password=new_url.password,
        host=new_url.hostname,
        port=new_url.port
    )

    new_cursor = new_conn.cursor()

    setup(new_conn, new_cursor)

    new_conn.commit()
    new_cursor.close()
    new_conn.close()

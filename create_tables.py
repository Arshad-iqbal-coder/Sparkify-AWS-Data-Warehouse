import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Drops all staging and analytics tables in Redshift.
    
    Parameters:
    cur : cursor
        Cursor object used to execute SQL queries.
    conn : connection
        Connection object to Redshift database.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
     """
    Creates all staging and analytics tables in Redshift.
    
    Parameters:
    cur : cursor
        Cursor object used to execute SQL queries.
    conn : connection
        Connection object to Redshift database.
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    
        config = configparser.ConfigParser()
        config.read('dwh.cfg')

        conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
        cur = conn.cursor()

        drop_tables(cur, conn)
        create_tables(cur, conn)

        conn.close()


if __name__ == "__main__":
    main()
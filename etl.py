import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Loads raw JSON data from S3 into Redshift staging tables using COPY commands.
    
    Parameters:
    cur : cursor
        Cursor object used to execute SQL queries.
    conn : connection
        Connection object to Redshift database.
    """
    for query in copy_table_queries:

        print("\n========================")
        print("Executing COPY Query")
        print("========================\n")

        print(query)

        try:
            cur.execute(query)
            conn.commit()

            print("\nCOPY SUCCESSFUL!\n")

        except Exception as e:
            print("\nCOPY FAILED!\n")
            print(e)

            conn.rollback()
    
    


def insert_tables(cur, conn):
      """
    Inserts transformed data from staging tables into analytics tables.
    
    Parameters:
    cur : cursor
        Cursor object used to execute SQL queries.
    conn : connection
        Connection object to Redshift database.
    """
    for query in insert_table_queries:
        print("Running INSERT query...")
        cur.execute(query)
        conn.commit()


def main():
    """
    Connects to Redshift and runs the ETL pipeline.
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
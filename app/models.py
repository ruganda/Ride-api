import psycopg2


class Database:
    """This class does all database related stuff"""

    def __init__(self):
        '''Initiates a database connection'''
        self.conn = psycopg2.connect(
            "dbname='ride_db' user='postgres' host = 'localhost' password='15december' port='5432'"
        )
        self.cur = self.conn.cursor()

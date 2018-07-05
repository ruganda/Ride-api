"""This module handles database queries"""
from urllib.parse import urlparse
import psycopg2
from werkzeug.security import generate_password_hash
from flask import current_app as app


class Database:
    """This class does all database related stuff"""

    def __init__(self, database_url):
        parsed_url = urlparse(database_url)
        d_b = parsed_url.path[1:]
        username = parsed_url.username
        hostname = parsed_url.hostname
        password = parsed_url.password
        port = parsed_url.port

        self.conn = psycopg2.connect(
            database=d_b, user=username, password=password,
            host=hostname, port=port)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def create_tables(self):
        """Creates database tables """
        create_table = "CREATE TABLE IF NOT EXISTS users\
        (id SERIAL PRIMARY KEY, name text, username text, password text)"
        self.cur.execute(create_table)

        create_table = "CREATE TABLE IF NOT EXISTS rides\
        (id SERIAL PRIMARY KEY, origin text, destination\
        text, date TIMESTAMP NOT NULL, driver text)"
        self.cur.execute(create_table)

        create_table = "CREATE TABLE IF NOT EXISTS requests\
        (id SERIAL PRIMARY KEY, ride_id INTEGER, status text, passenger text)"
        self.cur.execute(create_table)
        self.conn.commit()
        self.conn.close()

    def trancate_table(self, table):
        """Trancates the table"""
        self.cur.execute("TRUNCATE TABLE {} RESTART IDENTITY".format(table))

    def get_argument(self, table, column, arg):
        """
        Gets an urgument from the database column from a given table
        """
        self.cur.execute(
            "SELECT * FROM {} WHERE '{}' = '{}'"
            .format(table, column, arg))

        arg_object = self.cur.fetchone()
        return arg_object

    def fetch_all(self):
        """ Fetches all ride recods from the database"""
        self.cur.execute("SELECT * FROM rides ")
        rows = self.cur.fetchall()
        rides = []
        for row in rows:
            row = {'id': row[0], 'origin': row[1],
                   'destination': row[2],
                   'date': row[3], "driver": row[4]
                   }
            rides.append(row)
        return rides

    def insert_user_data(self, data):
        query = "INSERT INTO users (name, username, password)\
            VALUES('{}','{}', '{}');".format(data['name'],
                                             data['username'],
                                             generate_password_hash
                                             (data['password']))
        self.cur.execute(query)
        self.conn.commit()

    def update_request(self, r_id, data):
        '''Updates the status in the database'''
        self.cur.execute("UPDATE requests SET status='{}' WHERE id='{}'"
                         .format(data['status'], r_id))

        self.conn.commit()

    def insert_ride_data(self, data, driver):
        """Insert a new ride record to the database"""
        query = "INSERT INTO rides (origin, destination, date, driver)\
        VALUES('{}', '{}', '{}', '{}');".format(data['origin'],
                                                data['destination'],
                                                data['date'], driver)
        self.cur.execute(query)
        self.conn.commit()

    def send_request(self, ride_id, passenger):
        query = "INSERT INTO requests (ride_id, status, passenger)\
         VALUES('{}','{}', '{}');".format(ride_id, 'requested', passenger)
        self.cur.execute(query)
        self.conn.commit()

    def fetch_by_id(self, r_id):
        """ Gets a ride by id from the requests table"""
        self.cur.execute(
            "SELECT * FROM requests WHERE ride_id = '{}'".format(r_id))
        rows = self.cur.fetchall()
        requests = []
        for row in rows:
            requests.append({'Id': row[0], 'ride_id': row[1],
                             'status': row[2], 'passenger': row[3]})
        return requests

    def fetch_single_user(self, username):
        """Gets a single user by id from the database"""
        self.cur.execute(
            "SELECT * FROM users WHERE username = '{}'".format(username))
        user = self.cur.fetchone()
        return user

    def fetch_single_element(self, r_id):
        """selects a single ride by id from the database"""
        self.cur.execute(
            "SELECT * FROM rides WHERE id = '{}'".format(r_id))
        row = self.cur.fetchone()
        return row

    def fetch_by_ride(self, r_id):
        """ Gets a ride by id from the requests table"""
        self.cur.execute(
            "SELECT * FROM requests WHERE ride_id = '{}'".format(r_id))
        rows = self.cur.fetchone()

    def find_by_id(self, r_id):
        """selects a single ride by id from the database"""
        self.cur.execute(
            "SELECT * FROM rides WHERE id = '{}'".format(r_id))
        row = self.cur.fetchone()
        return row

import psycopg2


class Database:
    """This class does all database related stuff"""

    def __init__(self):
        '''Initiates a database connection'''
        self.conn = psycopg2.connect(
            "dbname='ride_db' user='postgres' host = 'localhost'\
             password='15december' port='5432'"
        )
        self.cur = self.conn.cursor()


class User(Database):

    def __init__(self, user_id=0, name=None, username=None, password=None):
        Database.__init__(self)
        self.user_id = user_id
        self.name = name
        self.username = username
        self.password = password
        self.rides_given = 0
        self.rides_taken = 0

    def get_single_user(self, username):
        self.cur.execute(
            "SELECT * FROM users WHERE username = '{}'".format(username))
        user = self.cur.fetchone()
        return user

    def insert_data(self, user):
        """Adds a new record to the database"""
        self.cur.execute(
            "INSERT INTO users (name, username, password, rides_taken, rides_given)\
             VALUES('{}','{}', '{}','{}','{}');"
            .format(user.name, user.username, user.password, self.rides_taken,
                    self.rides_given))
        self.conn.commit()


class Ride(Database):
    '''  Defines a Ride class'''

    def __init__(self, id=None, origin=None, destination=None, date=None):
        ''' Initializes the ride object'''
        self.instance = Database.__init__(self)
        self.id = id
        self.origin = origin
        self.destination = destination
        self.date = date

    def find_by_id(self, r_id):
        """selects a single ride by id from the database"""
        self.cur.execute(
            "SELECT * FROM rides WHERE id = %(id)s", {'id': r_id})

        row = self.cur.fetchone()
        if row:
            RIDE = {'id': row[0], 'origin': row[1],
                    'destination': row[2], 'date': row[3], "driver": row[4]}
            return RIDE

    def insert(self, driver):
        """Insert a new ride record to the database"""
        query = "INSERT INTO rides (origin, destination, date, driver)\
         VALUES(%s, %s, %s, %s)"
        self.cur.execute(query, (self.origin, self.destination,
                                 self.date, driver))
        self.conn.commit()

    def fetch_all(self):
        """ Fetches all ride recods from the database"""
        self.cur.execute("SELECT * FROM rides ")
        ROWS = self.cur.fetchall()
        RIDES = []
        for row in ROWS:
            print(row)
            row = {'id': row[0], 'origin': row[1],
                   'destination': row[2],
                   'date': row[3], "driver": row[4]
                   }
            RIDES.append(row)
            # print(RIDES)
        return RIDES

    def fetch_all_by_driver(self, driver):
        """ Fetches all ride recods of a driver from the database"""
        self.cur.execute("SELECT * FROM rides WHERE driver = %(driver)s",
                         {'driver': driver})
        ROWS = self.cur.fetchall()
        RIDES = []
        for row in ROWS:
            RIDES.append({'id': row[0], 'origin': row[1],
                          'destination': row[2],
                          'date': row[3], "driver": row[4]
                          })
        return RIDES


class Request(Database):
    ''' Defines the Request class'''

    def __init__(self, id=None, ride_id=None, status="requested",
                 passenger=None):
        Database.__init__(self)
        self.id = id
        self.ride_id = ride_id
        self.status = status
        self.passenger = passenger

    def insert(self, r_id, passenger):
        query = "INSERT INTO requests (ride_id, status, passenger)\
         VALUES('{}','{}', '{}');"\
            .format(r_id, self.status, passenger)
        self.cur.execute(query)
        self.conn.commit()

    def find_by_id(self, r_id):
        self.cur.execute(
            "SELECT * FROM requests WHERE ride_id = %(ride_id)s",
            {'ride_id': r_id})
        rows = self.cur.fetchall()
        REQUESTS = []
        for row in rows:
            REQUESTS.append({'Id': row[0], 'ride_id': row[1],
                             'status': row[2], 'passenger': row[3]})
        return REQUESTS

    def update_request(self, rId, data):
        '''Updates the status in the database'''
        self.cur.execute("UPDATE requests SET status=%s WHERE id=%s",
                         (data['status'], rId))
        self.conn.commit()

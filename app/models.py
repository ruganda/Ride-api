from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2


class Database:
    """This class does all database related stuff"""

    def __init__(self):
        '''Initiates a database connection'''
        self.conn = psycopg2.connect(
            "dbname='ride_db' user='postgres' host = 'localhost' password='15december' port='5432'"
        )
        self.cur = self.conn.cursor()
    
class User(Database):
    
    def __init__(self, user_id=0, name=None, username=None, password=None):
        Database.__init__(self)
        self.user_id = user_id
        self.name = name
        self.username = username
        self.password = generate_password_hash(password, method='sha256')      
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
            "INSERT INTO users (name, username, password, rides_taken, rides_given) VALUES('{}','{}', '{}','{}','{}');"
                       .format(user.name, user.username, user.password, self.rides_taken, self.rides_given))
        self.conn.commit()
    
class Ride(Database):
    '''  Defines a Ride class'''

    def __init__(self,id=None, origin=None, destination=None, date =None):
        ''' Initializes the ride object'''
        self.instance = Database.__init__(self)
        self.id = id
        self.origin = origin
        self.destination = destination
        self.date = date
    

    def find_by_id(self, r_id):
        self.cur.execute(
            "SELECT * FROM rides WHERE id = %(id)s", {'id': r_id})

        row = self.cur.fetchone()
        if row:
            ride = {'id': row[0], 'origin': row[1],
                             'destination': row[2], 'date': row[3], "driver": row[4]}
        self.conn.close()        
        return ride
    
    def insert(self, driver):
        
        query = "INSERT INTO rides (origin, destination, date, driver) VALUES(%s, %s, %s, %s)"
        self.cur.execute(query, (self.origin, self.destination,
                               self.date, driver))
        self.conn.commit()
    
    def fetch_all(self):
        """ Fetches all ride recods from the database"""
        self.cur.execute("SELECT * FROM rides ")
        rows = self.cur.fetchall()
        rides = []
        for row in rows:
            print(row)
            rides.append({'id': row[0], 'origin': row[1],
                             'destination': row[2], 'date': row[3], "driver": row[4]})
        
        return rides
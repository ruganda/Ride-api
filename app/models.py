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
    
    
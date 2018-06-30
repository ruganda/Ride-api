import unittest
import psycopg2
from flask import json
from app import create_app


class TestBase(unittest.TestCase):
    """ Base class for all test classess """
    app = create_app('TESTING')
    app.app_context().push()
    client = app.test_client()

    valid_user = {
        'name': 'TestUser',
        'username': 'validuser',
        'password': 'password'
    }

    valid_ride = {
        'origin': 'test origin',
        'destination': "test destination",
        "date": "2018-11-12 12:49:00"
    }
    post_ride = {
        'origin': 'origin',
        'destination': "test destination",
        "date": "2019-11-12 12:49:00"
    }

    def setUp(self):
        self.create_valid_user()
        self.delete_valid_ride()

    def create_valid_user(self):
        """ Registers a user to be used for tests"""
        response = self.client.post('/api/v2/auth/register',
                                    data=json.dumps(self.valid_user),
                                    content_type='application/json')
        return response

    def delete_valid_user(self):
        """Deletes valid user after tests"""
        connection = psycopg2.connect(
            "dbname='ride_db' user='postgres' host='localhost'\
             password='15december' port ='5432'")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE username = %s",
                       (self.valid_user['username'],))
        connection.close()

    def get_token(self):
        ''' Generates a toke to be used for tests'''
        response = self.client.post('/api/v2/auth/login',
                                    data=json.dumps(self.valid_user),
                                    content_type='application/json')
        data = json.loads(response.data.decode())
        return data['token']

    def create_valid_ride(self):
        """ Creates a valid ride to be used for tests """
        response = self.client.post('api/v2/rides/',
                                    data=json.dumps(self.valid_ride),
                                    content_type='application/json',
                                    headers={'Authorization':
                                             self.get_token()})
        return response

    def delete_valid_ride(self):
        """ Deletes the valid ride after tests """
        connection = psycopg2.connect(
            "dbname='ride_db' user='postgres' host='localhost'\
             password='15december' port ='5432'")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM rides WHERE origin = %s",
                       (self.valid_ride['origin'],))
        connection.close()

    def create_post_ride(self):
        """ Creates a valid ride to be used for tests """
        response = self.client.post('api/v2/rides/',
                                    data=json.dumps(self.post_ride),
                                    content_type='application/json',
                                    headers={'Authorization':
                                             self.get_token()})
        return response

    def delete_post_ride(self):
        """ Deletes the valid ride after tests """
        connection = psycopg2.connect(
            "dbname='ride_db' user='postgres' host='localhost'\
             password='15december' port ='5432'")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM rides WHERE origin = %s",
                       (self.post_ride['origin'],))
        connection.close()

    def delete_test_user(self):
        connection = psycopg2.connect(
            "dbname='ride_db' user='postgres' host='localhost'\
             password='15december' port ='5432'")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE username = %s", ('username',))
        connection.commit()
        connection.close()

    def tearDown(self):
        self.delete_valid_user()
        self.delete_valid_ride()
        self.delete_post_ride()

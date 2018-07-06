import unittest
import psycopg2
from flask import json
from app import create_app
from app.database import Database


class TestBase(unittest.TestCase):
    """ Base class for all test classess """
    app = create_app('TESTING')
    app.app_context().push()
    client = app.test_client()

    passenger = {
        'name': 'passenger name',
        'username': 'passenger',
        'password': 'password'
    }

    valid_user = {
        'name': 'TestUser',
        'username': 'validuser',
        'password': 'password'
    }

    valid_ride = {
        'origin': 'origin',
        'destination': "destination",
        "date": "2018-11-12 12:49:00"
    }
    post_ride = {
        'origin': 'kampala',
        'destination': "destination",
        "date": "2019-11-12 12:49:00"
    }

    def setUp(self):
        db = Database(
            'postgresql://postgres:15december@localhost:5432/test_db')
        db.create_tables()
        self.create_valid_user()

    def create_valid_user(self):
        """ Registers a user to be used for tests"""
        response = self.client.post('/api/v2/auth/register',
                                    data=json.dumps(self.valid_user),
                                    content_type='application/json')
        return response

    def get_token(self):
        ''' Generates a toke to be used for tests'''
        response = self.client.post('/api/v2/auth/login',
                                    data=json.dumps(self.valid_user),
                                    content_type='application/json')
        data = json.loads(response.data.decode())
        return data['token']

    def create_valid_ride(self):
        """ Creates a valid ride to be used for tests """
        response = self.client.post('api/v2/users/rides/',
                                    data=json.dumps(self.valid_ride),
                                    content_type='application/json',
                                    headers={'Authorization':
                                             self.get_token()})
        return response

    def create_post_ride(self):
        """ Creates a valid ride to be used for tests """
        response = self.client.post('api/v2/users/rides/',
                                    data=json.dumps(self.post_ride),
                                    content_type='application/json',
                                    headers={'Authorization':
                                             self.get_token()})
        return response

    def create_passenger(self):
        """ Registers a user to be used for tests"""
        response = self.client.post('/api/v2/auth/register',
                                    data=json.dumps(self.passenger),
                                    content_type='application/json')
        return response

    def passenger_token(self):
        ''' Generates a toke to be used for tests'''
        response = self.client.post('/api/v2/auth/login',
                                    data=json.dumps({
                                        'username': 'passenger',
                                        'password': 'password'}),
                                    content_type='application/json')
        data = json.loads(response.data.decode())
        return data['token']

    def tearDown(self):
        db = Database(
            'postgresql://postgres:15december@localhost:5432/test_db')
        db.trancate_table("users")
        db.trancate_table("rides")
        db.trancate_table("requests")

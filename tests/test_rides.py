import unittest
from flask import json
from test_base import TestBase


class Testride(TestBase):
    """ Defines tests for the view methods of rides """

    def setUp(self):
        self.create_valid_user()

    def test_accessing_ride_view_without_token(self):
        """ Tests accessing the ride endpoint without a token """
        response = self.client.get('/api/v2/rides/')
        self.assertEqual(response.status_code, 401)

    def test_accessing_ride_view_with_invalid_or_expired_token(self):
        """ Tests accessing the ride endpoint with an invalid
        or expired token """
        response = self.client.get('/api/v2/rides/',
                                   headers={'Authorization':
                                            'XBA5567SJ2K119'})
        self.assertEqual(response.status_code, 401)

    def test_create_ride_with_valid_details(self):
        """ Tests adding a ride with valid details """
        response = self.create_valid_ride()
        self.assertEqual(response.status_code, 201)
        self.delete_valid_ride()

    # def test_create_ride_with_blank_attributes(self):
    #     """ Tests creating a ride with a blank origin or destination """
    #     ride = {
    #         'origin': '',
    #         'destination': '',
    #         'date':''
    #     }
    #     response = self.client.post('/api/v2/rides/',
    #                                 data=json.dumps(ride),
    #                                 content_type='application/json',
    #                                 headers={'Authorization':
    #                                          self.get_token()})
    #     self.assertEqual(response.status_code, 400)

    # def test_create_duplicate_ride(self):
    #     """ Tests creating a duplicate ride (same attributes) """
    #     self.create_valid_ride()
    #     response = self.create_valid_ride()
    #     self.assertEqual(response.status_code, 409)
    #     self.delete_valid_ride()

    def test_get_rides(self):
        """ Tests fetching all rides  """
        self.create_valid_ride()
        response = self.client.get('/api/v2/rides/',
                                   headers={'Authorization':
                                            self.get_token()})
        self.assertEqual(response.status_code, 200)
        self.delete_valid_ride()

    def test_get_rides_valid_id(self):
        """ Tests querying a rides by a valid ID """

        response = self.client.get('/api/v2/rides/1' ,
                                   headers={'Authorization':
                                            self.get_token()})
        self.assertEqual(response.status_code, 200)
        self.delete_valid_ride()

    def test_rides_view_with_invalid_id(self):
        """ Tests querying for a ride with a none existent ID """
        response = self.client.get('/api/v2/rides/x',
                                   headers={'Authorization':
                                            self.get_token()})
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        self.delete_valid_user()

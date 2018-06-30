from flask import json
from test_base import TestBase


class Testride(TestBase):
    """ Defines tests for the view methods of rides """

    def setUp(self):
        self.create_valid_user()
        self.delete_post_ride()

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

    def test_make_ride_with_past_date(self):
        """ Tests creating a ride with a past date """
        response = self.create_valid_ride()
        ride = {
            'origin': 'an origin',
            'destination': 'a destination',
            "date": "2010-11-12 12:49:00"
        }
        response = self.client.post('/api/v2/users/rides/',
                                    data=json.dumps(ride),
                                    content_type='application/json',
                                    headers={'Authorization':
                                             self.get_token()})
        self.assertEqual(response.status_code, 406)
        self.assertIn("ride cannot have a past date and time",
                      str(response.data))

    def test_make_ride_with_ivalid_date_fomart(self):
        """ Tests creating a ride with an invalid date fomart"""
        response = self.create_valid_ride()
        ride = {
            'origin': 'an origin',
            'destination': 'a destination',
            "date": "12-11-2019 "
        }
        response = self.client.post('/api/v2/users/rides/',
                                    data=json.dumps(ride),
                                    content_type='application/json',
                                    headers={'Authorization':
                                             self.get_token()})
        self.assertEqual(response.status_code, 406)
        self.assertIn(
            "incorrect date and time format, should be YYYY-MM-DD HH:MM:SS",
            str(response.data))

    # def test_create_ride_with_valid_details(self):
    #     """ Tests adding a ride with valid details """
    #     response = self.create_post_ride()
    #     self.assertEqual(response.status_code, 201)
    #     self.delete_post_ride()

    def test_create_ride_with_blank_attributes(self):
        """ Tests creating a ride with a blank origin or destination """
        ride = {
            'origin': '',
            'destination': '',
            'date': ''
        }
        response = self.client.post('/api/v2/users/rides/',
                                    data=json.dumps(ride),
                                    content_type='application/json',
                                    headers={'Authorization':
                                             self.get_token()})
        self.assertEqual(response.status_code, 406)

    def test_create_ride_with_invalid_characters(self):
        """ Tests creating a ride with a blank origin or destination """
        ride = {
            'origin': '@#$%',
            'destination': '@#$%',
            'date': '!@#$'
        }
        response = self.client.post('/api/v2/users/rides/',
                                    data=json.dumps(ride),
                                    content_type='application/json',
                                    headers={'Authorization':
                                             self.get_token()})
        self.assertEqual(response.status_code, 406)

    def test_create_duplicate_ride(self):
        """ Tests creating a duplicate ride (same attributes) """
        self.create_valid_ride()
        response = self.create_valid_ride()
        self.assertEqual(response.status_code, 409)
        self.delete_valid_ride()

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
        self.create_valid_ride()
        # response = self.client.get('/api/v2/rides/1',
        #                            headers={'Authorization':
        #                                     self.get_token()})
        response = self.client.get('api/v2/rides/',
                                   headers={'Authorization':
                                            self.get_token()
                                            })
        self.assertEqual(response.status_code, 200)
        RESULTS = json.loads(response.data.decode())
        for ride in RESULTS:
            print(ride)
            print(RESULTS)
            response = self.client.get('api/v2/rides/{}'
                                       .format(ride['id']),
                                       headers={'Authorization':
                                                self.get_token()
                                                })
            self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.status_code, 200)
            self.delete_valid_ride()

    def test_rides_view_with_invalid_id(self):
        """ Tests querying for a ride with a none existent ID """
        response = self.client.get('/api/v2/rides/x',
                                   headers={'Authorization':
                                            self.get_token()})
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        self.delete_valid_user()
        self.delete_post_ride()

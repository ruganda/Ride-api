# import unittest
# from flask import json
import psycopg2
from test_base import TestBase
from flask import json


class TestRequest(TestBase):
    """ Defines tests for the view methods of requests """

    def setUp(self):
        self.create_valid_user()
        self.create_valid_ride()
        self.create_passenger()

    def test_join_request_issuccesful(self):
        """Test API can succesfully send a request to join
        a ride (POST request)"""
        response = self.client.post('api/v2/rides/1/requests',
                                    content_type='application/json',
                                    headers={'Authorization':
                                             self.passenger_token()
                                             })

        self.assertEqual(response.status_code, 201)

    def test_user_cannot_request_own_ride(self):
        """Test if a user can request to join his own ride"""
        response = self.client.post('api/v2/rides/1/requests',
                                    content_type='application/json',
                                    headers={'Authorization':
                                             self.get_token()
                                             })
        self.assertEqual(response.status_code, 403)

    def test_users_can_only_view_their_own_ride_requests(self):
        """Test if user can view ride request of a ride he did not create"""
        response = self.client.get('api/v2/users/rides/1/requests',
                                   headers={'Authorization':
                                            self.passenger_token()
                                            })
        self.assertEqual(response.status_code, 404)

    def test_respond_to_request_with_accepted(self):
        """Tests if a driver can respond to a ride request with accepted"""
        response = self.client.put('api/v2/users/rides/1/requests/1',
                                   content_type='application/json',
                                   data=json.dumps({'status': 'accepted'}),
                                   headers={'Authorization':
                                            self.get_token()
                                            })
        self.assertEqual(response.status_code, 200)
        self.assertIn('you have accepted this ride request',
                      str(response.data))

    def test_respond_to_request_with_rejected(self):
        """Tests if a driver can respond to a ride request with rejected"""
        response = self.client.put('api/v2/users/rides/1/requests/1',
                                   content_type='application/json',
                                   data=json.dumps({'status': 'rejected'}),
                                   headers={'Authorization':
                                            self.get_token()
                                            })
        self.assertEqual(response.status_code, 200)
        self.assertIn('you have rejected this ride request',
                      str(response.data))

    def test_respond_to_other_users_requests(self):
        """
        Tests if a user can respond to ride requests for rides
         he did not create
        """
        response = self.client.put('api/v2/users/rides/1/requests/1',
                                   content_type='application/json',
                                   data=json.dumps({'status': 'rejected'}),
                                   headers={'Authorization':
                                            self.passenger_token()
                                            })
        self.assertEqual(response.status_code, 404)

    def test_respond_to_request_with_invalid_status(self):
        """Tests sending reponding without accepted/rejected """
        response = self.client.put('api/v2/users/rides/1/requests/1',
                                   content_type='application/json',
                                   data=json.dumps({'status': 'invalid'}),
                                   headers={'Authorization':
                                            self.get_token()
                                            })
        self.assertEqual(response.status_code, 406)

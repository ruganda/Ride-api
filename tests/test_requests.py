# import unittest
# from flask import json
import psycopg2
from test_base import TestBase
from flask import json


class TestRequest(TestBase):
    """ Defines tests for the view methods of requests """

    def setUp(self):
        self.create_valid_user()
        self.create_valid_ride

    # def test_join_request_issuccesful(self):
    #     """Test API can succesfully send a request to join 
    #     a ride (POST request)"""
    #     response = self.client.post('api/v2/rides/1/requests',
    #                                 content_type='application/json',
    #                                 headers={'Authorization':
    #                                          self.get_token()
    #                                          })
        
    #     self.assertEqual(response.status_code, 201)

    def test_send_duplicate_ride(self):
        """Test send a duplicate ride request"""
        self.client.post('api/v2/rides/1/requests',
                                    content_type='application/json',
                                    headers={'Authorization':
                                             self.get_token()
                                             })
        response = self.client.post('api/v2/rides/1/requests',
                                    content_type='application/json',
                                    headers={'Authorization':
                                             self.get_token()
                                             })
        print(response.data)
        self.assertEqual(response.status_code, 409)

    def test_driver_can_get_all_ride_requests(self):
        """Test API can succesfully get all ride requests (GET request)"""
        response = self.client.get('api/v2/rides/1/requests',
                                   headers={'Authorization':
                                            self.get_token()
                                            })
        self.assertEqual(response.status_code, 200)

    def test_respond_to_request(self):
        """Tests if a driver can respond to a ride request succesfully"""
        response = self.client.put('api/v2/rides/1/requests/1',
                                    content_type='application/json',
                                    data=json.dumps({'status':'accepted'}),
                                    headers={'Authorization':
                                            self.get_token()
                                            })
        self.assertEqual(response.status_code, 200)

    def test_respond_to_request_with_invalid_status(self):
        """Tests sending reponding without accepted/rejected """
        response = self.client.put('api/v2/rides/1/requests/1',
                                    content_type='application/json',
                                    data=json.dumps({'status':'invalid'}),
                                    headers={'Authorization':
                                            self.get_token()
                                            })
        self.assertEqual(response.status_code, 406)

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
        self.delete_post_ride()

    def test_join_ride_request_is_successful(self):
        """Test accepting a ride request successfully(PUT)"""

        response = self.create_post_ride()
        response = self.client.get('api/v2/users/rides/',
                                   headers={'Authorization':
                                            self.get_token()
                                            })
        self.assertEqual(response.status_code, 200)
        RESULTS = json.loads(response.data.decode())

        for ride in RESULTS:
            if ride["origin"] == self.post_ride['origin'] and\
                    ride["destination"] == self.post_ride['destination'] and\
                    ride["date"] == self.post_ride['date']:
                response = self.client.post('api/v2/rides/{}/requests'
                                            .format(ride['id']),
                                            content_type='application/json',
                                            headers={'Authorization':
                                                     self.get_token()
                                                     })
                self.assertEqual(response.status_code, 201)
                self.assertIn(
                    "A request to join this ride has been sent",
                    str(response.data))

    def test_send_duplicate_ride_request(self):
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
        response = self.client.get('api/v2/users/rides/1/requests',
                                   headers={'Authorization':
                                            self.get_token()
                                            })
        self.assertEqual(response.status_code, 200)

    # def test_respond_to_request_with_invalid_status(self):
    #     """Tests sending reponding without accepted/rejected """
    #     response = self.client.put('api/v2/users/rides/1/requests/1',
    #                                content_type='application/json',
    #                                data=json.dumps({'status': 'invalid'}),
    #                                headers={'Authorization':
    #                                         self.get_token()
    #                                         })
    #     self.assertEqual(response.status_code, 406)

    def test_accept_request_issuccesful(self):
        """Test accepting a ride request successfully(PUT)"""

        response = self.create_post_ride()
        response = self.client.get('api/v2/users/rides/',
                                   headers={'Authorization':
                                            self.get_token()
                                            })
        self.assertEqual(response.status_code, 200)
        RESULTS = json.loads(response.data.decode())

        for ride in RESULTS:
            if ride["origin"] == self.post_ride['origin'] and\
                    ride["destination"] == self.post_ride['destination'] and\
                    ride["date"] == self.post_ride['date']:
                response = self.client.post('api/v2/rides/{}/requests'
                                            .format(ride['id']),
                                            content_type='application/json',
                                            headers={'Authorization':
                                                     self.get_token()
                                                     })
                self.assertEqual(response.status_code, 201)
                response = self.client.get('api/v2/rides/{}/requests'
                                           .format(ride['id']),
                                           content_type='application/json',
                                           headers={'Authorization':
                                                    self.get_token()
                                                    })
                self.assertEqual(response.status_code, 200)
                REQUESTS = json.loads(response.data.decode())
                for request in REQUESTS:
                    res = self.client.put('api/v2/rides/{}/requests/{}'
                                          .format(ride['id'],
                                                  request['id']),
                                          content_type='application/json',
                                          data=json.dumps(
                                              {'status': 'accepted'}),
                                          headers={'Authorization':
                                                   self.get_token()
                                                   })
                    self.assertEqual(res.status_code, 200)
                    self.assertIn(
                        'you have accepted this ride request', res.data)

    def test_Reject_request_issuccesful(self):
        """Test accepting a ride request successfully (PUT)"""

        response = self.create_post_ride()
        response = self.client.get('api/v2/users/rides/',
                                   headers={'Authorization':
                                            self.get_token()
                                            })
        self.assertEqual(response.status_code, 200)
        RESULTS = json.loads(response.data.decode())

        for ride in RESULTS:
            if ride["origin"] == self.post_ride['origin'] and\
                    ride["destination"] == self.post_ride['destination'] and\
                    ride["date"] == self.post_ride['date']:
                response = self.client.post('api/v2/rides/{}/requests'
                                            .format(ride['id']),
                                            content_type='application/json',
                                            headers={'Authorization':
                                                     self.get_token()
                                                     })
                self.assertEqual(response.status_code, 201)
                response = self.client.get('api/v2/rides/{}/requests'
                                           .format(ride['id']),
                                           content_type='application/json',
                                           headers={'Authorization':
                                                    self.get_token()
                                                    })
                self.assertEqual(response.status_code, 200)
                REQUESTS = json.loads(response.data.decode())
                for request in REQUESTS:
                    res = self.client.put('api/v2/rides/{}/requests/{}'
                                          .format(ride['id'],
                                                  request['id']),
                                          content_type='application/json',
                                          data=json.dumps(
                                              {'status': 'accepted'}),
                                          headers={'Authorization':
                                                   self.get_token()
                                                   })
                    self.assertEqual(res.status_code, 200)
                    self.assertIn(
                        'you have rejected this ride request', res.data)

    def test_Respond_with_an_invalid_status(self):
        """Test responding to a ride request with invalid status(PUT)"""
        self.delete_post_ride()
        response = self.create_post_ride()
        response = self.client.get('api/v2/users/rides/',
                                   headers={'Authorization':
                                            self.get_token()
                                            })
        self.assertEqual(response.status_code, 200)
        RESULTS = json.loads(response.data.decode())

        for ride in RESULTS:
            if ride["origin"] == self.post_ride['origin'] and\
                    ride["destination"] == self.post_ride['destination'] and\
                    ride["date"] == self.post_ride['date']:
                response = self.client.post('api/v2/rides/{}/requests'
                                            .format(ride['id']),
                                            content_type='application/json',
                                            headers={'Authorization':
                                                     self.get_token()
                                                     })
                self.assertEqual(response.status_code, 201)
                response = self.client.get('api/v2/rides/{}/requests'
                                           .format(ride['id']),
                                           content_type='application/json',
                                           headers={'Authorization':
                                                    self.get_token()
                                                    })
                self.assertEqual(response.status_code, 200)
                REQUESTS = json.loads(response.data.decode())
                for request in REQUESTS:
                    res = self.client.put('api/v2/rides/{}/requests/{}'
                                          .format(ride['id'],
                                                  request['id']),
                                          content_type='application/json',
                                          data=json.dumps(
                                              {'status': 'accepted'}),
                                          headers={'Authorization':
                                                   self.get_token()
                                                   })
                    self.assertEqual(response.status_code, 406)

    def test_respond_to_request_to_None_existing_ride(self):
        """Tests if a driver can respond to a none existing ride"""
        response = self.client.put('api/v2/users/rides/1000/requests/1',
                                   content_type='application/json',
                                   data=json.dumps({'status': 'accepted'}),
                                   headers={'Authorization':
                                            self.get_token()
                                            })
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        self.delete_valid_user()
        self.delete_valid_ride()
        self.delete_post_ride()

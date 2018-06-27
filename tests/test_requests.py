# import unittest
# from flask import json
# import psycopg2
# from test_base import TestBase


# class TestRequest(TestBase):
#     """ Defines tests for the view methods of requests """

#     def setUp(self):   
#         self.create_valid_user()
#         self.create_valid_ride
#     def test_join_request_issuccesful(self):
#         """Test API can succesfully send a request to join 
#         a ride (POST request)"""    
#         response = self.client.post('api/v2/rides/1/requests',
#                                     content_type='application/json',
#                                     data=json.dumps({}))
#         self.assertEqual(response.status_code, 201)
#         self.assertIn(
#             "A request to join this ride has been sent",
#             str(response.data))

#     def test_driver_can_get_all_ride_requests(self):
#         """Test API can succesfully get all ride requests (GET request)"""    
#         response = self.client.get('api/v2/rides/1/requests')
#         self.assertEqual(response.status_code, 200)
    
#     def test_respond_to_request(self):
#         """Tests if a driver can respond to a ride request succesfully"""
#         response = self.client.put('api/v2/rides/1/requests/1',
#                                     content_type='application/json',
#                                     data=json.dumps({'respond':'accept'}))
#         self.assertEqual(response.status_code, 200)
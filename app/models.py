"""This module handles database queries"""


class User:
    """This class does all database related stuff for the user"""

    def __init__(self, user_id, name, username, password):
        self.user_id = user_id
        self.name = name
        self.username = username
        self.password = password


class Ride:
    '''  Defines a Ride class'''

    def __init__(self, ride_id, origin, destination, date_time, driver):
        ''' Initializes the ride object'''
        self.ride_id = ride_id
        self.origin = origin
        self.destination = destination
        self.date_time = date_time
        self.driver = driver


class Request:
    ''' Defines the Request class'''

    def __init__(self, request_id, ride_id, status,
                 passenger):

        self.request_id = request_id
        self.ride_id = ride_id
        self.status = status
        self.passenger = passenger

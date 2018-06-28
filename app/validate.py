from datetime import datetime
import re


def validate_user(data):
    """validates the user and return appropriate message"""
    if not data['name'].strip() or not data['username'].strip() or not data['password'].strip():
        return "all fields are required"
    elif not re.match("^[a-zA-Z0-9_ ]*$", data['name'].strip()):
        return "Name should only contain alphanemeric characters"
    elif not re.match("^[a-zA-Z0-9_ ]*$", data['username'].strip()):
        return "username should only contain alphanemeric characters"
    elif not re.match("^[a-zA-Z0-9_]*$", data['password'].strip()):
        return "Password should only contain alphanemeric characters "
    else:
        return 'valid'


def validate_login(data):
    """validates the user and return appropriate message"""
    if not data['username'].strip() or not data['password'].strip():
        return "all fields are required"
    elif not re.match("^[a-zA-Z0-9_ ]*$", data['username'].strip()):
        return "username should only contain alphanemeric characters"
    elif not re.match("^[a-zA-Z0-9_]*$", data['password'].strip()):
        return "Password should only contain alphanemeric characters "
    else:
        return 'valid'


def validate_ride(data):
    """validates the rides inputs and return appropriate message"""
    if not 'origin' in data or not 'destination' in data or not 'date' in data:
        return "all fields are required"
    elif not re.match("^[a-zA-Z0-9_ ]*$", data['origin'].strip()):
        return "ride origin should only contain alphanemeric characters "
    elif not re.match("^[a-zA-Z0-9_ ]*$", data['destination'].strip()):
        return "ride location should only contain alphanemeric characters"
    else:
        return 'valid'


def validate_date(date_time):
    """check that the ride date and time is not past"""
    try:
        date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return "incorrect date and time format, should be YYYY-MM-DD HH:MM:SS"
    if date_time < datetime.now():
        return "ride cannot have a past date and time"
    return 'valid'

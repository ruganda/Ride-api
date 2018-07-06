from flask import jsonify


def not_found(error):
    """Handles a 404 error"""
    response = {
        "message": "Resource not found, Check the url and try again"
    }
    return jsonify(response), 404


def bad_request(error):
    """Handles a 400 error, bad request"""
    response = {
        "message": "Please check your inputs, inputs" +
        " should be in JSON format"
    }
    return jsonify(response), 400


def internal_server_error(error):
    """Handles a 500 error"""
    response = {
        "message": "something went wrong while processing " +
        "this request, please try again"
    }
    return jsonify(response), 500


def method_not_allowed(error):
    """Handles a 405 error"""
    response = {
        "message": "Method not allowed!" +
        " please check your request method "
    }
    return jsonify(response), 405

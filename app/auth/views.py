"""This module handles handles registering endponts"""
from flask import Blueprint
from app.auth.api import RegistrationView, LoginView

AUTH_BLUEPRINT = Blueprint('auth', __name__)

# Define the API resource
REGISTRATION_VIEW = RegistrationView.as_view('REGISTRATION_VIEW')
LOGIN_VIEW = LoginView.as_view('LOGIN_VIEW')

# Add the url rule for registering a user
AUTH_BLUEPRINT.add_url_rule(
    '/api/v2/auth/register',
    view_func=REGISTRATION_VIEW,
    methods=['POST'])
AUTH_BLUEPRINT.add_url_rule(
    '/api/v2/auth/login',
    view_func=LOGIN_VIEW,
    methods=['POST']
)

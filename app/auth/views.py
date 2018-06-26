from app.auth.api import RegistrationView
from flask import Blueprint

auth_blueprint = Blueprint('auth', __name__)


# Define the API resource
registration_view = RegistrationView.as_view('registration_view')


# Add the url rule for registering a user
auth_blueprint.add_url_rule(
    '/api/v2/auth/register',
    view_func=registration_view,
    methods=['POST'])

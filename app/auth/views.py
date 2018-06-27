from flask import Blueprint
from app.auth.api import RegistrationView, LoginView

auth_blueprint = Blueprint('auth', __name__)

# Define the API resource
registration_view = RegistrationView.as_view('registration_view')
login_view = LoginView.as_view('login_view')

# Add the url rule for registering a user
auth_blueprint.add_url_rule(
    '/api/v2/auth/register',
    view_func=registration_view,
    methods=['POST'])
auth_blueprint.add_url_rule(
    '/api/v2/auth/login',
    view_func=login_view,
    methods=['POST']
)
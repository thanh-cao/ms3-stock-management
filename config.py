import os
if os.path.exists('env.py'):
    import env


class ConfigClass(object):
    """ Flask application config """
    # Flask settings
    MONGODB_SETTINGS = {
        'db': os.environ.get('MONGO_DBNAME'),
        'host': os.environ.get('MONGO_URI'),
    }
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Flask-User settings
    USER_APP_NAME = "Book Repository"
    USER_ENABLE_EMAIL = False         # Disable email authentication
    USER_ENABLE_USERNAME = True       # Enable username authentication
    USER_ENABLE_CONFIRM_EMAIL = False  # Disable email after registration
    USER_ENABLE_FORGOT_PASSWORD = False  # Disable email after forgot password
    USER_ENABLE_CHANGE_PASSWORD = False  # Disable email after password change
    USER_SEND_PASSWORD_CHANGED_EMAIL = False  # Enable email after password change
    USER_REQUIRE_RETYPE_PASSWORD = True
    USER_ENABLE_CHANGE_USERNAME = False
    USER_AUTO_LOGIN_AFTER_REGISTER = True
    USER_AUTO_LOGIN_AT_LOGIN = True
    CSRF_ENABLED = True
    USER_APP_NAME = 'Stock Manager'

    # Flask-User redirecting endpoints
    USER_AFTER_REGISTER_ENDPOINT = 'profile'
    USER_AFTER_LOGIN_ENDPOINT = 'profile'
    USER_AFTER_LOGOUT_ENDPOINT = 'user.login'

    # Flask-User templates endpoints
    USER_REGISTER_TEMPLATE = 'signup.html'
    USER_LOGIN_TEMPLATE = 'login.html'

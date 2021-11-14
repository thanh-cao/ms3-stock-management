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
    USER_ENABLE_EMAIL = True         # Enable email authentication
    USER_ENABLE_USERNAME = False       # Disable username authentication
    USER_ENABLE_CONFIRM_EMAIL = True  # Enable email after registration
    USER_ENABLE_FORGOT_PASSWORD = False  # Disable email after forgot password
    USER_ENABLE_CHANGE_PASSWORD = False  # Disable password change
    USER_SEND_PASSWORD_CHANGED_EMAIL = False  # Disable email password change
    USER_REQUIRE_RETYPE_PASSWORD = True
    USER_ENABLE_CHANGE_USERNAME = False
    USER_AUTO_LOGIN_AFTER_REGISTER = True
    USER_AUTO_LOGIN_AT_LOGIN = True
    CSRF_ENABLED = True
    USER_APP_NAME = 'StockMGMT'
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = os.environ.get('USER_EMAIL_SENDER_EMAIL')

    # Flask-User redirecting endpoints
    USER_AFTER_REGISTER_ENDPOINT = 'account'
    USER_AFTER_LOGIN_ENDPOINT = 'dashboard'
    USER_AFTER_LOGOUT_ENDPOINT = 'user.login'

    # Flask-User templates endpoints
    USER_REGISTER_TEMPLATE = 'signup.html'
    USER_LOGIN_TEMPLATE = 'login.html'

    # Flask-User mail SMTP server setting
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')

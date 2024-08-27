import os

def get_admin_credentials():
    admin_login = os.environ.get('ADMIN_LOGIN')
    admin_password = os.environ.get('ADMIN_PASSWORD')
    admin_credentials = {
        'Login': admin_login,
        'Password': admin_password
    }
    return admin_credentials

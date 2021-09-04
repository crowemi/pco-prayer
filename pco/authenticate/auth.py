import json
import requests

class Auth(): 

    APP_ID = None
    SECRET = None

    def __init__(app_id, secret): 
        APP_ID = app_id if app_id is not None else None
        SECRET = secret if secret is not None else None

        if not APP_ID: 
            raise Exception("No APP_ID specified.")

        if not SECRET: 
            raise Exception("No SECRET specified.")

        
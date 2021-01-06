from collections import namedtuple
import re
import requests
from classeviva.model import Grade


BASE_URL = 'https://web.spaggiari.eu/rest/v1'

Credentials = namedtuple('Credentials', ['username', 'password'])
Identity = namedtuple('Identity', [
    'user_id',
    'ident',
    'token',
    'firstName',
    'lastName',
    'release',
    'expire',
])


class Client(object):

    def __init__(self, credentials):
        self.creds = credentials

    def __enter__(self):

        self.session = requests.Session()
        self.session.headers["User-Agent"] = "zorro/1.0"
        self.session.headers["Z-Dev-Apikey"] = "+zorro+"
        self.session.headers["Content-Type"] = "application/json"

        data = {
            "uid": self.creds.username,
            "pass": self.creds.password
        }
        resp = self.session.post(BASE_URL + "/auth/login/", json=data)
        if resp.status_code != 200:
            raise Exception('login failed: ' + resp.text)
        
        # from JSON to a dictionary
        _identity = resp.json()

        # The user ID is made of the `ident` without the leading
        # and trailing characters.
        _identity['user_id'] = re.sub(r"\D", "", _identity['ident'])

        self.identity = Identity(**_identity)
        # self.identity.id = re.sub(r"\D", "", self.identity.ident)

        # Add the token to the session, so it
        # will be used in all HTTP requests sent
        # from this client
        self.session.headers["Z-Auth-Token"] = self.identity.token
        
        return self

    def __exit__(self, *args):
        pass

    def grades(self):
        resp = self.session.get(url=BASE_URL + "/students/" + self.identity.user_id + "/grades")
        if resp.status_code != 200:
            raise Exception(resp.text)

        grades = resp.json()

        return [Grade(
            value=g['decimalValue'],
            display_value=g['displayValue'],
            subject=g['subjectDesc'],
            # kind=g['componentDesc'],
            date=g['evtDate'],
            comment=g['notesForFamily'],
        ) for g in grades['grades']]
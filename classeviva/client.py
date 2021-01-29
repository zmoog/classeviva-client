from collections import namedtuple
from datetime import datetime
import logging
import re

import requests
import pytz
from dateutil import parser

from classeviva.model import Grade


BASE_URL = 'https://web.spaggiari.eu/rest/v1'
HEADERS = {
    "User-Agent": "zorro/1.0",
    "Z-Dev-Apikey": "+zorro+",
    "Content-Type": "application/json",
}

Credentials = namedtuple('Credentials', [
    'username',
    'password'
])
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
    """Client for the Classe Viva API"""

    def __init__(self, credentials):
        self._identity_manager = CachedIdentityManager(
            username=credentials.username,
            password=credentials.password,
        )

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def grades(self):
        """Return the list of ``Grade``s for the user."""

        _identity = self._identity_manager.get_identity()
        headers = {
            "Z-Auth-Token": _identity.token
        }

        # add standard HTTP headers
        headers.update(HEADERS)

        resp = requests.get(
            url=BASE_URL + "/students/" + _identity.user_id + "/grades", headers=headers)
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


# def _fetch_identity(username, password):

#     session = requests.Session()
#     session.headers["User-Agent"] = "zorro/1.0"
#     session.headers["Z-Dev-Apikey"] = "+zorro+"
#     session.headers["Content-Type"] = "application/json"
  
#     data = {
#         "uid": username,
#         "pass": password
#     }
#     resp = session.post(BASE_URL + "/auth/login/", json=data)
#     if resp.status_code != 200:
#         raise Exception('login failed: ' + resp.text)

#     # from JSON to a dictionary
#     _identity = resp.json()

#     # The user ID is made of the `ident` without the leading
#     # and trailing characters.
#     _identity['user_id'] = re.sub(r"\D", "", _identity['ident'])

#     identity = Identity(**_identity)

#     # Add the token to the session, so it
#     # will be used in all HTTP requests sent
#     # from this client
#     session.headers["Z-Auth-Token"] = identity.token

#     return session, identity


class CachedIdentityManager(object):

    def __init__(self, username, password):
        self.logger = logging.getLogger(__name__)
        self._username = username
        self._password = password
        self._identity = None

    def  get_identity(self,):
        now = datetime.now(tz=pytz.timezone('Europe/Rome'))
        if self._identity is None or self._identity.expire < now:
            print('getting new identity')
            self._identity = self._get_access_identity(
                self._username,
                self._password
            )
        else:
            print('reusing cached identity')
        return self._identity

    def _get_access_identity(self, username, password):
        data = {
            "uid": username,
            "pass": password
        }
        url = "{}/auth/login/".format(BASE_URL)
        resp = requests.post(url, json=data, headers=HEADERS)
        if resp.status_code != 200:
            raise Exception('login failed: ' + resp.text)

        # from JSON to a dictionary
        _identity = resp.json()

        # The user ID is made of the `ident` without the leading
        # and trailing characters.
        _identity['user_id'] = re.sub(r"\D", "", _identity['ident'])
        
        # replace the release and expire strings with a datetime
        _identity['release'] = parser.isoparse(_identity['release'])
        _identity['expire'] = parser.isoparse(_identity['expire'])

        return Identity(**_identity)


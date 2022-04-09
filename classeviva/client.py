import json
import re
from collections import namedtuple
from datetime import date, datetime, timedelta

import requests

from classeviva.model import Entry, Grade

BASE_URL = "https://web.spaggiari.eu/rest/v1"

Identity = namedtuple(
    "Identity",
    [
        "user_id",
        "ident",
        "token",
        "firstName",
        "lastName",
        "release",
        "expire",
        "showPwdChangeReminder",
    ],
)


class Client(object):
    def __init__(self, creds_provider):
        self.creds_provider = creds_provider

    def __enter__(self):
        creds = self.creds_provider()

        self.session = requests.Session()
        self.session.headers["User-Agent"] = "zorro/1.0"
        self.session.headers["Z-Dev-Apikey"] = "+zorro+"
        self.session.headers["Content-Type"] = "application/json"

        data = {"uid": creds.username, "pass": creds.password}
        resp = self.session.post(BASE_URL + "/auth/login/", json=data)
        if resp.status_code != 200:
            raise Exception("login failed: " + resp.text)

        # from JSON to a dictionary
        _identity = resp.json()

        # The user ID is made of the `ident` without the leading
        # and trailing characters.
        _identity["user_id"] = re.sub(r"\D", "", _identity["ident"])

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
        resp = self.session.get(
            url=f"{BASE_URL}/students/{self.identity.user_id}/grades"
        )
        if resp.status_code != 200:
            raise Exception(resp.text)

        grades = resp.json()

        return [
            Grade(
                value=g["decimalValue"],
                display_value=g["displayValue"],
                subject=g["subjectDesc"],
                # kind=g['componentDesc'],
                date=g["evtDate"],
                color=g["color"],
                comment=g["notesForFamily"],
            )
            for g in grades["grades"]
        ]

    def list_agenda(
        self,
        since: datetime.date = date.today(),
        until: datetime.date = date.today() + timedelta(days=5),
    ):
        _user_id = self.identity.user_id
        _since = since.strftime("%Y%m%d")
        _until = until.strftime("%Y%m%d")

        resp = self.session.get(
            f"{BASE_URL}/students/{_user_id}/agenda/all/{_since}/{_until}"
        )
        if resp.status_code != 200:
            raise Exception(resp.text)

        agenda = resp.json()

        return [
            Entry(
                id=g["evtId"],
                code=g["evtCode"],
                author=g["authorName"],
                notes=g["notes"],
                starts_at=g["evtDatetimeBegin"],
                ends_at=g["evtDatetimeEnd"],
                subject=g["subjectDesc"],
            )
            for g in agenda.get("agenda", [])
        ]

    def list_notes(self):
        resp = self.session.get(
            f"{BASE_URL}/students/{self.identity.user_id}/notes/all"
        )
        if resp.status_code != 200:
            raise Exception(resp.text)

        print(json.dumps(resp.json(), indent=2))

        return []

    def list_noticeboard(self):
        resp = self.session.get(
            f"{BASE_URL}/students/{self.identity.user_id}/noticeboard"
        )
        if resp.status_code != 200:
            raise Exception(resp.text)

        print(json.dumps(resp.json(), indent=2))

        return []

    def list_calendar(self):
        resp = self.session.get(
            f"{BASE_URL}/students/{self.identity.user_id}/calendar/all"
        )
        if resp.status_code != 200:
            raise Exception(resp.text)

        print(json.dumps(resp.json(), indent=2))

        return []

    def list_cards(self):
        resp = self.session.get(
            f"{BASE_URL}/students/{self.identity.user_id}/card"
        )
        if resp.status_code != 200:
            raise Exception(resp.text)

        print(json.dumps(resp.json(), indent=2))

        return []

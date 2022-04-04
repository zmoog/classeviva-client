from os import getenv
from typing import Any
from collections import namedtuple

Credentials = namedtuple('Credentials', ['username', 'password'])

class CredentialsNotFoundError(Exception):
    pass

class EnvCredentialsProvider:
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        username = getenv("CLASSEVIVA_USERNAME", None)
        password = getenv("CLASSEVIVA_PASSWORD", None)

        if not username or not password:
            raise CredentialsNotFoundError("Can't find credentials in the CLASSEVIVA_* environment variables")
        
        return Credentials(username, password)

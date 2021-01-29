# ClasseViva Client

ClasseViva Client is a tiny Python library to access the popular electronic register service used by a lot of schools in Italy.

## Usage

Here's how to use it to fetch the latest grades:

```python

from classeviva.client import Client, Credentials

credentials = Credentials(
    username="user@school.edu",
    password="secret!"
)

with Client(credentials) as client:
   grades = client.grades()

```

## Features

### Grades

### Python 2 Friendly

The library has been written to be also used in Python 2.x environments (for example, in project using [Alfred-Workflow](http://www.deanishe.net/alfred-workflow/) to build [Alfred 2, 3 and 4](https://www.alfredapp.com/) workflows).

# classeviva-client

classeviva-client is a Python library and a CLI tool to access the https://web.spaggiari.eu, probably the most used portal for schools, students and families.

## Getting Started

Set your credentials as environment variables:

```shel
export CLASSEVIVA_USERNAME="you@domain.com"
export CLASSEVIVA_PASSWORD="secret!"
```

### As a Python library

```shell
$ python
>>>
>>> from classeviva.client import Client
>>> from classeviva.credentials import EnvCredentialsProvider
>>>
>>>
>>> with Client(EnvCredentialsProvider()) as client:
...   print(client.grades()[:1])
...
[Grade(value=7.25, display_value='7+', subject='ITALIANO', date='2021-10-11', color='green', comment='')]
```

### As a CLI tool

List your grades:

```shell
$ classeviva list-grades

2022-03-30
- MUSICA, 7
2022-03-28
- MATEMATICA, 7½
2022-02-22
- MUSICA, 9½
- RELIGIONE, 8½
```

List your agenda entries for homework assignments:

```shell
$ classeviva list-agenda

2022-04-07
- TEACHER A, Geometria: pagina 42 n.90-91-96-100.
- TEACHER B, leggere e tradurre oralmente i dialogo di p. 130 e copiare una volta sul quaderno. 
```

## Refs

Special thanks to [@michelangelomo](https://github.com/michelangelomo) for providing good API docs at [michelangelomo/Classeviva-Official-Endpoints](https://github.com/michelangelomo/Classeviva-Official-Endpoints).

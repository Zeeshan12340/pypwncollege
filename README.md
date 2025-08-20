# PyPwnCollege

[![Run Tests](https://github.com/zeeshan12340/pypwncollege/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/zeeshan12340/pypwncollege/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/zeeshan12340/pypwncollege/branch/main/graph/badge.svg)](https://codecov.io/gh/zeeshan12340/pypwncollege)
[![Documentation Status](https://readthedocs.org/projects/pypwncollege/badge/?version=latest)](https://pypwncollege.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/PyPwnCollege.svg)](https://badge.fury.io/py/PyPwnCollege)
[![PyPI Statistics](https://img.shields.io/pypi/dm/pypwncollege.svg)](https://pypistats.org/packages/pypwncollege)

PyPwnCollege is an unofficial Python library to interact with the pwn.college API and website.

## Install

```bash
pip install pypwncollege
```

## Demo

> Note: Username/Password is not stored on the system, only the session cookie "app_cookie" is stored in ~/.pwncli.json. Re-login might be needed if that cookie expires.

```py
from pwncollege import PWNClient
# Create an API connection
client = PWNClient(email="user@example.com", password="S3cr3tP455w0rd!")
# Print the User associated with the client
print(client.user)
```

## CLI

The library also comes with a CLI to interact with the API which is a work in progress. It is included in the published pip package and should be available in shell.

Basic usage:

```bash
pwncli --help
pwncli login -u test1337 -p test1337
pwncli get --dojos
pwncli challenge -d fundamentals -m program-misuse -c level-1 -f flag{test}
```

> Note: Not specifying the password on the command line will make pwncli request it like sudo does.

## Documentation

The documentation is available [here](https://pypwncollege.readthedocs.io/en/latest/).

## Current Features

- Logging into the API
- Fetching Dojos, Modules, Challenges
  - Starting a Challenge
  - Running an ssh command on a challenge
  - Submitting flags
- Getting User details
- Getting rankings in dojos and modules
- Getting information about belted users

## Contributing

If you find a bug or want to add a feature, feel free to open an issue or a pull request.

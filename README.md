# PyPwnCollege

[![Documentation Status](https://readthedocs.org/projects/pypwncollege/badge/?version=latest)](https://pypwncollege.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/PyPwnCollege.svg)](https://badge.fury.io/py/PyPwnCollege)

PyPwnCollege is an unofficial Python library to interact with the pwn.college API and website.

## Install

```bash
pip install pypwncollege
```

## Demo

```py
from pwncollege import PWNClient
# Create an API connection
client = PWNClient(email="user@example.com", password="S3cr3tP455w0rd!")
# Print the User associated with the client
print(client.user)
```

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

PyPwnCollege
==================

``pypwncollege`` is an unofficial Python library designed to automate
accessing the pwncollege API.

Getting Started
---------------
Setting up an API connection::

    from pwncollege import PWNClient
    client = PWNClient(email="user@example.com", password="S3cr3tP455w0rd!")
    print(client.user)

For Getting a challenge, you need the dojo and module alongwith the challenge::
    
    dojos = client.get_dojos()
    modules = client.get_modules(dojos[0])
    challenges = client.get_challenges(dojos[0], modules[0])

    chall = client.create_challenge(dojos[0], modules[0], challenges[0])
    chall.start()
    chall.run("ls")

Module Index
---------------

.. toctree::
    :maxdepth: 3
    :glob:

    pwn
    challenge
    leaderboard
    user
    errors

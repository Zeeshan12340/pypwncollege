def main(client, testing=False):
    if testing:
        return
    dojos = client.get_dojos()
    modules = client.get_modules(dojos[0])
    challenges = client.get_challenges(dojos[0], modules[0])

    challenge = client.create_challenge(dojos[0], modules[0], challenges[0])
    challenge.start()

    challenge.run("ls -la")
    challenge.submit("pwn.college{practice}")


if __name__ == "__main__":
    from base import client as example_client

    main(example_client)

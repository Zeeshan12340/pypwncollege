from pwncollege import PWNClient

def test_login():
    """Tests the ability to login and receive a valid session token."""
    client = PWNClient(email='test1337', password='test1337')
    assert client._app_cookie is not None

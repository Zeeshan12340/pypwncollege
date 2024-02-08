from pwncollege import PWNClient
from pwncollege.utils import cookie_expired

def test_login():
    """Tests the ability to login and receive a valid session token."""
    client = PWNClient(email='test1337', password='test1337')
    assert cookie_expired(client._app_cookie) == False
    assert client._app_cookie is not None
    assert client.user.name == 'test1337'
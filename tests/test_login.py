from pwncollege import PWNClient

def test_login():
    """Tests the ability to login and receive a valid session token."""
    client = PWNClient(email='test1337', password='test1337')
    assert client._app_cookie is not None
    assert client.user.name == 'test1337'

def test_leaderboard():
    """Tests the ability to retrieve a leaderboard."""
    client = PWNClient(email='test1337', password='test1337')
    leaderboard = client.get_dojo_ranking("fundamentals")
    assert len(leaderboard.items) == 20

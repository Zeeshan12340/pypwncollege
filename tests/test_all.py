from pwncollege import PWNClient
from pwncollege.utils import cookie_expired

client = PWNClient(email='test1337')
def test_login():
    """Tests the ability to login and receive a valid session token."""
    assert cookie_expired(client._app_cookie) == False
    assert client._app_cookie is not None
    assert client.user.name == 'test1337'

def test_leaderboard():
    """Tests the ability to retrieve a leaderboard."""
    leaderboard = client.get_dojo_ranking("fundamentals")
    assert len(leaderboard.items) == 20
    
def test_challenge():
    """Tests the ability to start and submit a challenge."""
    dojos = client.get_dojos()
    assert dojos != []
    
    modules = client.get_modules(dojos[0])
    assert modules != []
    
    challenges = client.get_challenges(dojos[0], modules[0])
    assert challenges != []
    
    challenge = client.create_challenge(dojos[0], modules[0], challenges[0])
    instance = challenge.start()
    assert instance.dojo == dojos[0]
    assert instance.module == modules[0]
    assert instance.chall_id == challenge.id

    # Do the challenge.....
    assert challenge.submit("123") is False
    
from pwncollege import PWNClient

def test_leaderboard():
    """Tests the ability to retrieve a leaderboard."""
    client = PWNClient(email='test1337', password='test1337')
    leaderboard = client.get_dojo_ranking("fundamentals")
    assert len(leaderboard.items) == 20
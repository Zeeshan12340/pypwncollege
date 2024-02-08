from typing import List, Iterator

from . import pwncollege


class Leaderboard(pwncollege.PWNObject):
    """The class representing a Leaderboard

    Args:
        data: A list of Leaderboard entries

    """

    items: List[str]

    def __len__(self):
        return len(self.items)

    def __init__(self, data: List[dict], client: pwncollege.PWNClient):
        self._client = client
        self.items = [usr["name"] for usr in data]
        

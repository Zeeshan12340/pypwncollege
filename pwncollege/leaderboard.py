from typing import List, Iterator

from . import pwncollege


class Leaderboard(pwncollege.PWNObject):
    """The class representing a Leaderboard

    Args:
        data: A list of Leaderboard entries

    """

    items: List[str]
    _iter: Iterator[None]

    def __getitem__(self, key):
        return self.items[key]

    def __iter__(self):
        # noinspection PyTypeChecker
        self._iter = iter(self.items)
        return self

    def __next__(self):
        return next(self._iter)

    def __len__(self):
        return len(self.items)

    def __init__(self, data: List[dict], client: pwncollege.PWNClient):
        self._client = client
        self.items = [usr["name"] for usr in data]
        

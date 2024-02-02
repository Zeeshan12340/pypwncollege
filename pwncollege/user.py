from typing import TYPE_CHECKING

from . import pwncollege

if TYPE_CHECKING:
    from .pwncollege import PWNClient


class User(pwncollege.PWNObject):
    """The class representing pwncollege Users

    Attributes:
        name: The username of the User
        ranking: The User's position on the Global Leaderboard
        points: The User's current total points
        country_name: The name of the User's country

        website: The User's website
        belt: The User's current belt

    """

    name: str
    ranking: int
    points: int
    website: str

    country_name: str
    belt: str


    def __repr__(self):
        return f"<User '{self.name}'>"

    # noinspection PyUnresolvedReferences
    def __init__(self, data: dict, client: "PWNClient"):
        """Initialise a `User` using API data"""
        self._client = client
        self.id = data["id"]

        self.name = data["name"]
        self.points = data["points"]
        self.ranking = data["ranking"]
        self.website = data["website"]
        
        self.country_name = data["country_name"]
        self.belt = data["belt"]


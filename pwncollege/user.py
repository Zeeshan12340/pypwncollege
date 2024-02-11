from typing import TYPE_CHECKING

from . import pwncollege
from pwncollege.pwncollege import colors
from .utils import parse_csrf_token

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

    def change_profile(self, new_username: str = None, new_email: str = None, password: str = None, new_website: str = None, new_country: str = None, hidden: str = "False"):
        """Change the User's username"""
        """get nonce"""
        nonce = parse_csrf_token(self._client.do_request("/settings").text)
        
        json_data = {}
        if new_username:
            json_data["name"] = new_username
            self.name = new_username
        if new_email:
            if password is None:
                raise ValueError("Password is required to change email")
            json_data["email"] = new_email
        if password:
            json_data["password"] = password
            json_data["confirm"] = password
        if new_website:
            json_data["website"] = new_website
            self.website = new_website
        if new_country:
            json_data["country"] = new_country
            self.country_name = new_country
        if hidden == "True" or hidden == "False":
            json_data["hidden"] = hidden
        json_data["fields"] = []
            
        res = self._client.do_request(
            "/api/v1/users/me",
            json_data=json_data,
            patch=True,
            nonce=nonce
        ).json()

        if res["success"]:
            print(colors.green +
                  f"Changes successful!" + colors.reset)
            if new_username:
                print(f"Username: {res['data']['name']}")
            if new_email:
                print(f"Email: {res['data']['email']}")
            if new_website:
                print(f"Website: {res['data']['website']}")
            if new_country:
                print(f"Country: {res['data']['country']}")
        else:
            print(res["errors"])

from typing import TYPE_CHECKING, Any, Dict

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
        country: The name of the User's country
        university: The name of the User's university

        website: The User's website
        belt: The User's current belt

    """

    name: str
    ranking: int
    points: int
    website: str
    university: str

    country: str
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

        self.country = data["country"]
        self.belt = data["belt"]
        self.university = data["university"]

    def change_profile(self, new_username: str = "", new_email: str = "", password: str = "", new_website: str = "", new_country: str = "", new_university: str = "", hidden: str = "False"):
        """Change the User's username"""
        """get nonce"""
        nonce = parse_csrf_token(self._client.do_request("/settings").text)

        json_data: Dict[str, Any] = {}
        if new_username:
            json_data["name"] = new_username
            self.name = new_username
        if new_email:
            if password:
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
            self.country = new_country
        if new_university:
            json_data["university"] = new_university
            self.university = new_university
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
            if new_university:
                print(f"University: {res['data']['university']}")
        else:
            print(res["errors"])

    def change_sshkey(self, ssh_key: str):
        """Change the User's SSH key"""
        nonce = parse_csrf_token(self._client.do_request("/settings").text)
        json_data = {
            "ssh_key": ssh_key
        }
        res = self._client.do_request(
            "pwncollege_api/v1/ssh_key",
            json_data=json_data,
            patch=True,
            nonce=nonce
        ).json()

        if res["success"]:
            print(colors.green +
                  f"Changes successful - SSH Public Key set!" + colors.reset)
        else:
            print(colors.red +
                  "Changes failed!" + colors.reset)
            print(res["errors"])

from __future__ import annotations

import atexit
import getpass
import json
import os
import re
from typing import List, Union, Optional, cast, TYPE_CHECKING

import requests

from .constants import SITE_BASE, USER_AGENT
from .errors import (
    AuthenticationException,
    ServerErrorException,
)
from .utils import cookie_expired, parse_csrf_token

if TYPE_CHECKING:
    from .user import User
    from .challenge import Challenge
    from .leaderboard import Leaderboard

class colors:
    """ANSI color codes for use in terminal output

    Examples:
        Using colors::
            print(colors.red + "Hello, world!" + colors.reset)

    """
    red = "\033[91m"
    green = "\033[92m"
    yellow = "\033[93m"
    blue = "\033[94m"
    reset = "\033[0m"

class PWNClient:
    """The client via which API requests are made

    Examples:
        Connecting to the API::

            from pwncollege import PWNClient
            client = PWNClient(email="user@example.com", password="S3cr3tP455w0rd!")
            client = PWNClient(email="unique1234", password="S3cr3tP455w0rd!")
            value for email can also be username

    """

    _user: Optional["User"] = None
    _app_cookie: Optional[str] = None
    _site_base: str
    nonce: Optional[str] = None
    session: requests.Session = requests.Session()


    def __init__(
        self,
        email: Optional[str] = None,
        password: Optional[str] = None,
        cache: Optional[str] = None,
        site_base: str = SITE_BASE,
        app_cookie: Optional[str] = None,
    ):
        """
        Authenticates to the API.

        If `cache` is set, the client will attempt to load access tokens from the given path. If they cannot be found,
        or are expired, normal API authentication will take place, and the tokens will be dumped to the file for the
        next launch.

        Args:
            email: The authenticating user's email address
            password: The authenticating user's password
            cache: The path to load/store access tokens from/to
            app_cookie: Authenticate using a provided App Cookie
        """
        self._site_base = site_base
        if cache is not None:
            if self.load_from_cache(cache) is False:
                print(f"{colors.yellow}[!] Failed to load from cache, logging in normally{colors.reset}")
                self.do_login(email, password, app_cookie)
                self.dump_to_cache(cache)
            # Make sure we dump our current tokens out when we exit
            atexit.register(self.dump_to_cache, cache)
        else:
            self.do_login(email, password, app_cookie)


    def do_request(
        self,
        endpoint,
        json_data=None,
        data=None,
        post=False,
        nonce: Optional[str] = None,
    ) -> requests.Response:
        """

        Args:
            endpoint: The API/normal endpoint to request
            json_data: Data to be sent in JSON format
            data: Data to be sent in application/x-www-form-urlencoded format
            post: Force POST request
        Returns:
            The JSON response from the API or the raw response if not JSON

        """
        headers = {
            "User-Agent": USER_AGENT,
            "Csrf-Token": nonce,
        }
    
        if not json_data and not data:
            if post:
                r = self.session.post(
                    self._site_base + endpoint, headers=headers
                )
            else:
                r = self.session.get(
                    self._site_base + endpoint, headers=headers
                )
        else:
            r = self.session.post(
                self._site_base + endpoint,
                json=json_data,
                data=data,
                headers=headers,
            )
            
        if r.status_code >= 500:
            raise ServerErrorException(f"Server error: {r.status_code}")
        else:
            return r

    def load_from_cache(self, cache: str) -> bool:
        """
        Args:
            cache: The cache file path

        Returns: Whether loading from the cache was successful
        """
        if not os.path.exists(cache):
            return False
        
        with open(cache, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return False
        self._app_cookie = data.get("app_cookie")
        if self._app_cookie is None or cookie_expired(self._app_cookie):
            return False
        
        print(f"{colors.green}[+] Loaded from cache!{colors.reset}")
        return True

    def dump_to_cache(self, cache):
        """
        Dumps the current access and refresh tokens to a file
        Args:
            cache: The path to the cache file
        """
        if not os.path.exists(os.path.dirname(cache)):
            return
        
        with open(cache, "w") as f:
            json.dump(
                {
                    "app_cookie": self._app_cookie,
                },
                f,
            )

    def do_login(
        self,
        email: Optional[str] = None,
        password: Optional[str] = None,
        app_cookie: Optional[str] = None,
    ):
        """
        Authenticates against the API. If credentials are not provided, they will be prompted for.
        """

        if app_cookie is not None:
            self._app_cookie = app_cookie
            return self._app_cookie
        
        if email is None:
            email = input(colors.blue + "Enter your username or email? " + colors.reset)
        if password is None:
            password = getpass.getpass()

        if self.nonce is None:
            first = self.do_request("login")
            self.nonce = parse_csrf_token(first.text)
            print(f"{colors.green}[+] CSRF token: {colors.reset}{colors.blue}{self.nonce}{colors.reset}")

        data = self.do_request(
            "login",
            data={
                "name": email,
                "password": password,
                "_submit": "Submit",
                "nonce": self.nonce,
            }
        )
        if "Your username or password is incorrect" not in data.text:
            print(f"{colors.green}[+] Logged in as {colors.reset}{colors.blue}{email}!{colors.reset}")
            self._app_cookie = self.session.cookies.get("session")
            return self._app_cookie
        else:
            raise AuthenticationException("Incorrect username or password")


    def get_dojos(self) -> List[str]:
        """Requests a list of available dojos

        Returns: A list of dojos

        """
        data = self.do_request("dojos").text
        dojos = re.findall("href=\"/dojo/(.*)\"", data)
        return dojos
    
    def get_modules(self, dojo: str) -> List[str]:
        """Requests a list of available modules in a dojo
        
        Args:
            dojo: The dojo to fetch modules from
        
        Returns: A list of modules
        """
        r = self.do_request(f"{dojo}/")
        if r.status_code == 404:
            print(f"{colors.red}[!] Dojo {dojo} does not exist!{colors.reset}")
            return []
        data = r.text
        modules = re.findall(f"href=\"/{dojo}/(.*)\"", data)
        return modules

    # noinspection PyUnresolvedReferences
    def get_challenges(self, dojo: str, module: str) -> List["Challenge"]:
        """Requests a list of `Challenge` from the API in a module

        Args:
            dojo: The dojo to fetch challenges from
            module: The module to fetch challenges from

        Returns: A list of `Challenge`

        """
        from .challenge import Challenge

        r = self.do_request(f"pwncollege_api/v1/dojo/{dojo}/{module}/challenges")
        if r.status_code == 404:
            print(f"{colors.red}[!] Dojo {dojo} or module {module} does not exist!{colors.reset}")
        data = cast(dict, r.json())

        # TODO: parse challenges html page for number of solves and solved challenges
        for challenge in data["challenges"]:
            challenge["dojo"] = dojo
            challenge["module"] = module
        
        challenges = [Challenge(challenge, self) for challenge in data["challenges"]]
        return challenges
    
    def create_challenge(self, dojo: str, module: str, chall: Challenge) -> "Challenge":
        """Creates a `Challenge` object from needed info"""
        from .challenge import Challenge

        data = {
            "id": chall.id,
            "dojo": dojo,
            "module": module,
            "challenge_id": chall.challenge_id,
        }
        return Challenge(data, self)

    # noinspection PyUnresolvedReferences
    def get_user(self, user_id: int) -> "User":
        """
        Args:
            user_id: The platform ID of the `User` to fetch

        Returns: The requested `User`

        """
        from .user import User

        text = self.do_request(f"/hacker/{user_id}").text
        name_re = re.search("<h1>(.*)</h1>", text)
        name = name_re.group(1) if name_re else ""
        score = self.do_request("/pwncollege_api/v1/score?username=" + name).text.strip('"').split(":")
        
        country = re.search("'country_name': \"([^\"]+)\"", text)
        country_name = country.group(1) if country else None

        belt_re = re.search("<img src=\"/themes/dojo_theme/static/img/dojo/(.*).svg", text)
        belt = belt_re.group(1) if belt_re else None
        website_re = re.search("<a href=\"(.*)\" target=\"_blank\" style=\"color: inherit;\" rel=\"noopener\">", text)
        website = website_re.group(1) if website_re else None

        data = cast(dict, {
            "id": user_id,
            "name": name,
            "points": score[1],
            "ranking": score[0],
            "website": website,
            "country_name": country_name,
            "belt": belt,
        })
        print(data)
        return User(data, self)

    # noinspection PyUnresolvedReferences
    def get_dojo_ranking(self, dojo: str, duration: int = 0, page: int = 1) -> "Leaderboard":
        """
        Returns: A Leaderboard of the top 20 Users in the Dojo
        """
        from .leaderboard import Leaderboard

        r = self.do_request(f"pwncollege_api/v1/scoreboard/{dojo}/_/{duration}/{page}")
        if r.status_code == 404:
            print(f"{colors.red}[!] Dojo {dojo} does not exist!{colors.reset}")

        data = cast(dict, r.json())["standings"]
        return Leaderboard(data, self)
    
    # noinspection PyUnresolvedReferences
    def get_module_ranking(self, dojo: str, module: str, duration: int = 0, page: int = 1) -> "Leaderboard":
        """
        Returns: A Leaderboard of the top 20 Users in the Module
        """
        from .leaderboard import Leaderboard

        r = self.do_request(f"pwncollege_api/v1/scoreboard/{dojo}/{module}/{duration}/{page}")
        if r.status_code == 404:
            print(f"{colors.red}[!] Dojo {dojo} or module {module} does not exist!{colors.reset}")

        data = cast(dict, r.json())["standings"]
        return Leaderboard(data, self)
    
    def get_belts(self) -> dict:
        """Requests a list of available belts

        Returns: A list of belts

        """
        data = self.do_request("pwncollege_api/v1/belts").json()
        return cast(dict, data)
    
    # noinspection PyUnresolvedReferences
    @property
    def user(self) -> "User":
        """

        Returns: The `User` associated with the current `PWNClient`

        """
        match = re.search("'userId': (\\d+)", self.do_request("/").text)
        assert match, "Failed to find User ID"
        uid = int(match.group(1))

        if not self._user:
            self._user = self.get_user(uid)
        return self._user

class PWNObject:
    """Base class of all API objects

    Attributes:
        id: The ID of the associated object
    """

    _client: PWNClient
    id: str


    def __eq__(self, other):
        return self.id == other.id and type(self) == type(other)

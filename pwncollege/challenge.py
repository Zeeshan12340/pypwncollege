"""
Examples:
    Starting a challenge and submitting the flag::

        challenge = client.get_challenge("<dojo>", "<module>", "<challenge_id>")
        (get dojo/module/challenge listings from client.get_dojos()/client.get_modules()/client.get_challenges())

        instance = challenge.start()
        challenge.interactive()

        # Do the challenge.....
        challenge.submit(flag)

"""

from __future__ import annotations

import os
import paramiko
import time
import json
from typing import cast, TYPE_CHECKING

from . import pwncollege
from .errors import (
    IncorrectArgumentException,
)
from .utils import parse_csrf_token

if TYPE_CHECKING:
    from .pwncollege import PWNClient


class Challenge(pwncollege.PWNObject):
    """The class representing pwncollege challenges

    Attributes:
        id (str): Module specific ID or name of level   
        challenge_id (int): Dojo specific challenge ID
        dojo (str): Dojo name
        module (str): Module name
        name (str): The name of the challenge
        description: The challenge description

        solves: The number of solves a challenge has
        solved: Whether the active user has completed the challenge
    """

    _client: "PWNClient"

    id: str
    challenge_id: int
    dojo: str
    module: str
    name: str
    description: str

    # solves: int
    # solved: bool

    def submit(self, flag: str):
        """Submits a flag for a Challenge

        Args:
            flag: The flag for the Challenge

        """
        # TODO: check if flag is already submitted
        nonce = parse_csrf_token(self._client.do_request("").text)
        submission = cast(
            dict,
            self._client.do_request(
                "api/v1/challenges/attempt",
                json_data={
                    "challenge_id": self.challenge_id,
                    "submission": flag,
                },
                nonce=nonce,
            ).json(),
        )

        if not submission["success"]:
            raise IncorrectArgumentException("Invalid submission!")
        if submission["data"]["status"] == "incorrect":
            print("Incorrect flag!")
            return False
        elif submission["data"]["status"] == "authentication_required":
            print("Please login again.")
            return False
        elif submission["data"]["status"] == "already_solved":
            print("You have already solved this challenge!")
        elif submission["data"]["status"] == "correct":
            print("Correct!")

        return True

    def connect(self):
        """Connects to the challenge via SSH"""
        res = self._client.do_request("pwncollege_api/v1/docker")
        if res.json()["success"] is False:
            print(res.json()["error"])
            print("Starting challenge...")
            self.start()

        self.sshclient.load_system_host_keys()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            self.sshclient.connect(
                "pwn.college",
                username="hacker",
                look_for_keys=True,
            )
        except paramiko.ssh_exception.AuthenticationException:
            print("Error connecting to pwn.college")
            return
        
    def start(self, practice: bool = False) -> DockerInstance:
        """
        Requests the challenge be started

        Args:
            practice: Whether to start a practice instance

        Returns:
            The DockerInstance that was started

        """
        nonce = parse_csrf_token(self._client.do_request("").text)
        response = self._client.do_request(
                "pwncollege_api/v1/docker",
                json_data={
                    "dojo": self.dojo,
                    "module": self.module,
                    "challenge": self.id,
                    "practice": practice,
                },
                nonce=nonce,
            )
        print(response.json())

        try:
            if not response.json()["success"]:
                raise IncorrectArgumentException(response.json()["success"])
        except json.JSONDecodeError:
            raise IncorrectArgumentException(response.json()["success"])
        
        print("Challenge started!")
        self.instance = DockerInstance(
            self.dojo, self.module, self.id, self._client
        )
        
        return self.instance

    def download(self, remote: str = "", local=None) -> str:
        """
        Downloads the challenges files located in /challenge by default
        Args:
            remote: The path of the file to download. Defaults to /challenge
            local: The name of the zipfile to download to. If none is provided, it is saved to the current directory.

        Returns: The path of the file

        """
        if local is None:
            local = os.path.join(os.getcwd(), f"{self.name}")
        elif self.instance is None:
            print("Challenge not started!")
            return

        sftp = self.sshclient.open_sftp()

        if remote == "":
            files = sftp.listdir("/challenge/")
            for file in files:
                remote = os.path.join("/challenge/", file)
                local = os.path.join(os.getcwd(), file)
                sftp.get(remote, local)
            sftp.close()
            return local

        sftp.get(remote, local)
        sftp.close()
        return local
    
    def run(self, command: str, system: bool = False):
        """Starts an interactive ssh session with the challenge"""
        if self.sshclient.get_transport() is None:
            print("Connecting to Challenge!")
            self.connect()
        
        if system:
            os.system("ssh hacker@pwn.college -t tmux")
            return

        try:
            channel = self.sshclient.invoke_shell()
            out = channel.recv(9999)

            channel.send((command + "\n").encode("latin-1"))
            while not channel.recv_ready():
                time.sleep(1)
            out = channel.recv(9999)
            print(out.decode("ascii"))

        except Exception as e:
            print("Error connecting to pwn.college")
            print(e)
            return
        

    def __repr__(self):
        return f"<Challenge '{self.name}'>"

    # noinspection PyUnresolvedReferences
    def __init__(self, data: dict, client: PWNClient):
        """Initialise a `Challenge` using API data"""
        self._client = client

        self.id = data["id"]
        self.challenge_id = data["challenge_id"]
        self.dojo = data["dojo"]
        self.module = data["module"]
        self.name = data["name"] if "name" in data else ""
        self.description = data["description"] if "description" in data else ""

        # self.solves = data["solves"]
        # self.solved = data["solved"]

        self.sshclient = paramiko.SSHClient()


class DockerInstance:
    """Representation of an active Docker container instance of a Challenge

    Attributes:
        dojo: The name of the dojo the instance is running in
        module: The name of the module the instance is running in
        chall_id: The connected challenge
        client: The passed-through API client

    """

    dojo: str
    module: str
    chall_id: str
    client: pwncollege.PWNClient

    def __init__(
        self,
        dojo: str,
        module: str,
        chall_id: str,
        client: pwncollege.PWNClient,
    ):
        self.client = client
        self.dojo = dojo
        self.module = module
        self.chall_id = chall_id

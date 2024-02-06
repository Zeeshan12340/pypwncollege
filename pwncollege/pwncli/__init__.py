#!/usr/bin/env python3
import argparse
from random import choice
import pwncollege
import os
from .challenge import challenge

def get_args():
    # Begin original commands - mostly related to authentication
    parser = argparse.ArgumentParser(
        description="Interact with pwncollege from the command line.",
        usage="pwncli [-h] [-c CACHE] [-v] {login,challenge} ..."
        )
    parser.add_argument('-c', '--cache', type=str, required=False, help='filesystem location for cache. Default is ~/.pwncli.json', default="~/.pwncli.json")
    subparsers = parser.add_subparsers(title='subcommands', dest='subcommand')

    # Begin login subcommand
    parser_login = subparsers.add_parser('login', help="Login to pwncollege. Stores session cookie in cache ")
    parser_login.add_argument('-u', '--username', required=False, help='Username/Email for pwncollege.')
    parser_login.add_argument('-p', '--password', required=False, help='Password for pwncollege. If not provided, will prompt.')

    # Begin get subcommand
    parser_get = subparsers.add_parser('get', help="Get dojos/modules and their scoreboards.")
    parser_get.add_argument('-d', '--dojos', required=False, help='Get listing of all available dojos')
    parser_get.add_argument('-m', '--modules', required=False, help='Get listing of all available modules in a dojo')
    parser_get.add_argument('-c', '--challenges', required=False, help='Get listing of all available challenges in a module inside a dojo')
    parser_get.add_argument('-dr', '--dojo-ranking', required=False, help='Get ranking of top users in a dojo')
    parser_get.add_argument('-mr', '--module-ranking', required=False, help='Get ranking of top users in a module inside a dojo')
    parser_get.add_argument('-b', '--belt', required=False, help='Get JSON data of all belted users')
    parser_get.add_argument('-i', '--info', required=False, help='Get information about your user')


    # Begin challenge subcommand
    parser_chall = subparsers.add_parser('challenge', help="Interact with challenges.")
    parser_chall.add_argument('-n', '--name', required=False, help='Name of the challenge, or the challenge ID.')
    parser_chall.add_argument('-p', '--path', type=str, help='Download challenge files to the specified path.', default=None)
    parser_chall.add_argument('-s', '--start-docker', action="store_true", help='Start Docker instance.')
    parser_chall.add_argument('-f', '--flag', type=str, help='Submit flag.')
    
    args = parser.parse_args()

    return args

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

class PWNCLI:
    def __init__(self) -> None:
        self.args = get_args()
        self.client = None

        if self.args == argparse.Namespace(cache=None, subcommand=None):
            print(colors.yellow + "Use the -h/--help flag for basic help information." + colors.reset)
            exit()

        self.subcommand = self.args.subcommand

    def login(self):
        """Login to pwncollege"""
        cache = os.path.expanduser(self.args.cache)

        if not os.path.exists(cache):
            if self.subcommand != 'login':
                print(colors.red + "You must login first." + colors.reset)
                exit()
            elif self.subcommand == 'login' and not self.args.username:
                print(colors.red + "Username is required." + colors.reset)
                exit()
            else:
                self.client = pwncollege.PWNClient(
                    email=self.args.username, password=self.args.password,
                    cache=cache)
        else:
            self.client = pwncollege.PWNClient(cache=cache)

    def run(self):
        """Executes the specified subcommand"""
        self.login()

        if self.subcommand == 'challenge':
            challenge(self)

def main():
    flavortext = [
        "Skill issue.",
        "when new challenges? SoonTM",
        ":feelsyanman:",
        "dojo broken 504 error :c",
        "check the man page",
        "man chmod",
        "it's too hard/ctfy/easy.That's your attitude to everything",
        "how get belts?!?!?",
        "If you're using Windows, don't.",
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA...",
        "Hello Hackers!!!",
        "zeeshan probably cheesed it :frowning:",
    ]

    print(f'\n\033[92mpwncli - v0.1.0 | {choice(flavortext)}\033[0m')
    print('\033[35mauthor: @Zeeshan12340 (www.zeeshan1234.tech)\033[0m\n')
    
    obj = PWNCLI()
    try:
        obj.run()
    except KeyboardInterrupt:
        print("\nExiting...")
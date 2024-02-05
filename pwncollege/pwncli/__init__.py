#!/usr/bin/env python3
import argparse
from random import choice
import pwncollege
import os

def get_args():
    # Begin original commands - mostly related to authentication
    parser = argparse.ArgumentParser(
        description="Interact with pwncollege from the command line.",
        usage="pwncli [-h] [-c CACHE] [-v] {login,challenge} ..."
        )
    parser.add_argument('-c', '--cache', type=str, help='Path to cached credentials.')
    parser.add_argument('-v', '--verbose', action="store_true", help="increase output verbosity")
    subparsers = parser.add_subparsers(title='subcommands', dest='subcommand')

    # Begin login subcommand
    parser_chall = subparsers.add_parser('login', help="Login to pwncollege. Stores session cookie in cache ")
    parser_chall.add_argument('-u', '--username', required=False, help='Username/Email for pwncollege.')
    parser_chall.add_argument('-p', '--password', required=False, help='Password for pwncollege. If not provided, will prompt.')
    parser_chall.add_argument('-c', '--cache', required=False, help='filesystem location for cache. Default is ~/.pwncli.json', default="~/.pwncli.json")

    # Begin challenge subcommand
    parser_chall = subparsers.add_parser('challenge', help="Interact with challenges.")
    parser_chall.add_argument('-n', '--name', required=True, help='Name of the challenge, or the challenge ID.')
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

        if self.args == argparse.Namespace(cache=None, subcommand=None, verbose=False):
            print(colors.yellow + "Use the -h/--help flag for basic help information." + colors.reset)
            exit()

        if self.args.verbose:
            self.print_args()

        self.subcommand = self.args.subcommand
        
    def login(self, username, password, cache):
        """Login to pwncollege"""
        if os.path.exists(cache):
            self.client = pwncollege.PWNClient(cache=cache)
            return

        if not username:
            print(colors.red + "Username is required." + colors.reset)
            exit()

        self.client = pwncollege.PWNClient(
            email=username, password=password,
            cache=cache)

    def run(self):
        """Executes the specified subcommand"""
        self.login(self.args.username, self.args.password, os.path.expanduser(self.args.cache))
        if self.subcommand == 'challenge':
            self.challenge()
        

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
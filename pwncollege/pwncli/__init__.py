#!/usr/bin/env python3
import argparse
from random import choice
import pwncollege
import os
from .challenge import challenge
from .get import get
from pwncollege.pwncollege import colors

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
    parser_get.add_argument('-d', '--dojos', required=False, action="store_true", help='Get listing of all available dojos')
    parser_get.add_argument('-m', '--modules', required=False, help='Get listing of all available modules in a dojo')
    parser_get.add_argument('-c', '--challenges', required=False, help='Get listing of all available challenges in a module inside a dojo')
    parser_get.add_argument('-dr', '--dojo-ranking', required=False, help='Get ranking of top users in a dojo')
    parser_get.add_argument('-mr', '--module-ranking', required=False, help='Get ranking of top users in a module inside a dojo')
    parser_get.add_argument('-b', '--belt', required=False, help='Get JSON data of all belted users')
    parser_get.add_argument('-i', '--info', required=False, nargs='?', const='0', help='Get information about your user(default) or a specific user by id(int).')


    # Begin challenge subcommand
    parser_chall = subparsers.add_parser('challenge', help="Interact with challenges.")
    parser_chall.add_argument('-d', '--dojo', required=False, help='Name of the dojo')
    parser_chall.add_argument('-m', '--module', required=False, help='Name of the module')
    parser_chall.add_argument('-c', '--challenge', required=False, help='Name of the challenge')
    parser_chall.add_argument('-r', '--practice', required=False, help='Start in practice mode. Default is False.', default=False, action='store_true')
    parser_chall.add_argument('-p', '--path', type=str, help='Download challenge files to the specified path.', default=os.getcwd())
    parser_chall.add_argument('-s', '--start-docker', action="store_true", help='Start Docker instance.')
    parser_chall.add_argument('-f', '--flag', type=str, help='Submit flag.')
    
    args = parser.parse_args()

    return args

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
        elif self.subcommand == 'login':
            self.client = pwncollege.PWNClient(cache=cache)
        else:
            self.client = pwncollege.PWNClient(cache=cache, notif=False)

    def run(self):
        """Executes the specified subcommand"""
        self.login()

        if self.subcommand == 'challenge':
            challenge(self)
        elif self.subcommand == 'get':
            get(self)
        elif self.subcommand != 'login':
            print(colors.yellow + "Use the -h/--help flag for basic help information." + colors.reset)
            exit()
            

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
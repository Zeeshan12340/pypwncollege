#!/usr/bin/env python3
import argparse
from random import choice
import pwncollege

def get_args():
    # Begin original commands - mostly related to authentication
    parser = argparse.ArgumentParser(
        description="Interact with pwncollege from the command line.",
        usage="pwncli [-h] [-c CACHE] [-v] {challenge,login} ..."
        )
    parser.add_argument('-c', '--cache', type=str, help='Path to cached credentials.')
    parser.add_argument('-v', '--verbose', action="store_true", help="increase output verbosity")
    subparsers = parser.add_subparsers(title='subcommands', dest='subcommand')

    # Begin challenge subcommand
    parser_chall = subparsers.add_parser('challenge', help="Interact with challenges.")
    parser_chall.add_argument('-n', '--name', required=True, help='Name of the challenge, or the challenge ID.')
    parser_chall.add_argument('-p', '--path', type=str, help='Download challenge files to the specified path.', default=None)
    parser_chall.add_argument('-s', '--start-docker', action="store_true", help='Start Docker instance.')
    parser_chall.add_argument('--stop', action="store_true", help='Stop challenge instance.')
    parser_chall.add_argument('-r', '--reset', action="store_true", help='Stop and then start challenge instance.')
    parser_chall.add_argument('-f', '--flag', type=str, help='Submit flag.')
    parser_chall.add_argument('-d', '--difficulty', type=int, choices=range(10,101), metavar="[10-100]", help='Submit difficulty rating, 10-100.')

    # Begin login subcommand
    parser_chall = subparsers.add_parser('login', help="login to pwncollege.")
    
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

        if self.args == argparse.Namespace(cache=None, subcommand=None, verbose=False):
            print(colors.yellow + "Use the -h/--help flag for basic help information." + colors.reset)
            exit()

        if self.args.verbose:
            self.print_args()

        self.subcommand = self.args.subcommand
        
    def run(self):
        """Executes the specified subcommand"""
        # self.cred_management()
        if self.subcommand == 'challenge':
            self.challenge()
        elif self.subcommand == 'login':
            pwncollege.PWNClient()
        

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
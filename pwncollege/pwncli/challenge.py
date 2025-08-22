from pwncollege.challenge import Challenge
import argparse

def challenge(self):
    """Challenge subcommand"""
    """if no flags, print help message"""
    if not self.args.dojo and not self.args.module and not self.args.challenge:
        subparsers_actions = [
            action for action in self.parser._actions 
            if isinstance(action, argparse._SubParsersAction)]
        for subparsers_action in subparsers_actions:
            for choice, subparser in subparsers_action.choices.items():
                if choice == "challenge":
                    print(subparser.format_help())
        exit()
        
    if self.args.dojo and not self.args.module and not self.args.challenge:
        print("You need module and challenge_id to start a challenge.")
        exit()
    
    elif self.args.dojo and self.args.module and not self.args.challenge:
        print("You need a challenge_id to start a challenge.")
        exit()
    
    elif self.args.dojo and self.args.module and self.args.challenge:
        """
        Everything is available, check if dojo, module, and challenge exist.
        If not, exit. If so, create challenge.
        """
        dojos = [dojo["id"] for dojo in self.client.get_dojos()]
        if self.args.dojo not in dojos:
            print("Dojo not found.")
            exit()
        modules = [module["id"] for module in self.client.get_modules(self.args.dojo)]
        if self.args.module not in modules:
            print("Module not found.")
            exit()
        
        challenges = self.client.get_challenge_ids(self.args.dojo, self.args.module)
        if self.args.challenge not in challenges:
            print("Challenge not found.")
            exit()

        dojo = self.args.dojo
        module = self.args.module
        challenge_id = challenges.get(self.args.challenge)
        data = {"id": self.args.challenge, "challenge_id": challenge_id,
                "dojo": dojo, "module": module}
        challenge = Challenge(data, self)
        self.myChall = self.client.create_challenge(dojo, module, challenge)

    if self.args.start_docker:
        if self.myChall is None:
            print("You need to specify dojo+module+challenge_id to start a challenge.")
            exit()
        self.myChall.start(practice=self.args.practice)

    if self.args.flag:
        if self.myChall is None:
            print("You need to specify dojo+module+challenge_id to submit a flag.")
            exit()
        self.myChall.submit(self.args.flag)

    if self.args.path:
        if self.myChall is None:
            print("You need to specify dojo+module+challenge_id to download challenge files.")
            exit()
        self.myChall.connect()
        self.myChall.download(remote="", local=self.args.path)
    
    if self.args.execute:
        if self.myChall is None:
            print("You need to specify dojo+module+challenge_id to execute a command.")
            exit()
        self.myChall.connect()
        self.myChall.run(command=self.args.execute)
    
    if self.args.interactive:
        if self.myChall is None:
            print("You need to specify dojo+module+challenge_id to start an interactive shell.")
            exit()
        self.myChall.connect()
        self.myChall.run(system=True)
    
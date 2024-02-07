from pwncollege.pwncollege import colors
from pwncollege.challenge import Challenge

def challenge(self):
    """Challenge subcommand"""
    """if no flags, print help message"""
    if not self.args.dojo and not self.args.module and not self.args.challenge:
        print(colors.yellow + "Use the -h/--help flag for basic help information." + colors.reset)
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
        if self.args.dojo not in self.client.get_dojos():
            print("Dojo not found.")
            exit()
        elif self.args.module not in self.client.get_modules(self.args.dojo):
            print("Module not found.")
            exit()
        
        challenges = [c for c in self.client.get_challenges(self.args.dojo, self.args.module)]
        challenge_ids = [c.id for c in challenges]
        if self.args.challenge not in challenge_ids:
            print("Challenge not found.")
            exit()

        dojo = self.args.dojo
        module = self.args.module
        challenge_id = next((c.challenge_id for c in challenges if c.id == self.args.challenge), None)
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
    
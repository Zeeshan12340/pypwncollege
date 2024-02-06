from pwncollege.pwncollege import colors

def get(self):
    if self.args.dojos:
        dojos = self.client.get_dojos()
        print("-"*12 + "Dojos" + "-"*13)
        for dojo in dojos:
            print("| " + dojo + " "*(27-len(dojo)) + "|")
        print("-" * 30)
    
    if self.args.modules:
        dojo = self.args.modules
        modules = self.client.get_modules(dojo)
        if modules == []:
            exit()
        print("-"*11 + "Modules" + "-"*12)
        for module in modules:
            print("| " + module + " "*(27-len(module)) + "|")
        print("-" * 30)
    
    if self.args.challenges:
        if not self.args.modules:
            print(colors.red + "You must specify a dojo using the -m/--modules flag." + colors.reset)
            exit()
        dojo = self.args.modules
        module = self.args.challenges
        challenges = self.client.get_challenges(dojo, module)
        if challenges == []:
            exit()
        print("-"*10 + "Challenges" + "-"*10)
        for challenge in challenges:
            print("| " + challenge.id + " "*(27-len(challenge.id)) + "|")
        print("-" * 30)
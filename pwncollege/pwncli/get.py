from pwncollege.pwncollege import colors
import json

def get(self):
    if self.args.dojos and not self.args.modules and not self.args.challenges:
        dojos = self.client.get_dojos()
        print("-"*12 + "Dojos" + "-"*13)
        for dojo in dojos:
            print("| " + dojo + " "*(27-len(dojo)) + "|")
        print("-" * 30)
    
    if self.args.modules and not self.args.challenges:
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
    
    if self.args.dojo_ranking and not self.args.module_ranking:
        dojo = self.args.dojo_ranking
        ranking = self.client.get_dojo_ranking(dojo)
        print("-"*9 + "Dojo Ranking" + "-"*9)
        for index, user in enumerate(ranking):
            print("| " + f"{index+1}. " + user + " "*(25-len(user)-len(str(index+1))) + "|")
        print("-" * 30)

    if self.args.module_ranking:
        if not self.args.dojo_ranking:
            print(colors.red + "You must specify a dojo using the -dr/--dojo-ranking flag." + colors.reset)
            exit()
        dojo = self.args.dojo_ranking
        module = self.args.module_ranking
        ranking = self.client.get_module_ranking(dojo, module)
        print("-"*8 + "Module Ranking" + "-"*8)
        for index, user in enumerate(ranking):
            print("| " + f"{index+1}. " + user + " "*(25-len(user)-len(str(index+1))) + "|")
        print("-" * 30)
    
    if self.args.belt:
        belt_color = self.args.belt
        valid_belts = ["orange", "yellow", "green", "blue", "black"]
        if belt_color not in valid_belts:
            print(colors.red + "Invalid belt color." + colors.reset)
            print(f"Valid belt colors: {', '.join(valid_belts)}")
            exit()
        belts = self.client.get_belts()["users"]
        for user in belts.values():
            if user["color"] == belt_color:
                print(json.dumps(user, indent=2))
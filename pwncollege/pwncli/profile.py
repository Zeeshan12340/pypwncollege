import argparse

def profile(self):
    """Change profile data such as username, ssh public key etc."""
    if not any([self.args.username, self.args.email, self.args.password, self.args.website, self.args.country, self.args.visibility, self.args.ssh_key]):
        subparsers_actions = [
            action for action in self.parser._actions 
            if isinstance(action, argparse._SubParsersAction)]
        for subparsers_action in subparsers_actions:
            for choice, subparser in subparsers_action.choices.items():
                if choice == "profile":
                    print(subparser.format_help())
        exit()
        
    if self.args.username:
        self.client.user.change_profile(new_username=self.args.username)
    if self.args.email:
        if not self.args.password:
            raise ValueError("Password is required to change email")
        self.client.user.change_profile(new_email=self.args.email, password=self.args.password)
    if self.args.password:
        self.client.user.change_profile(password=self.args.password)
    if self.args.website:
        self.client.user.change_profile(new_website=self.args.website)
    if self.args.country:
        self.client.user.change_profile(new_country=self.args.country)
    if self.args.visibility:
        self.client.user.change_profile(hidden=self.args.visibility)
    if self.args.ssh_key:
        self.client.change_ssh_key(self.args.ssh_key)
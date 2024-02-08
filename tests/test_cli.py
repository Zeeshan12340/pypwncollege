import pwncollege.pwncli as pwncli
import sys

sys.argv=['']

def test_cli():
    """
    Runs the CLI and checks for a successful exit code.
    Simulate argparse input.
    """
    pwncli.main()
    
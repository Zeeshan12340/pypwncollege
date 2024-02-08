import pwncollege.pwncli as pwncli
import os
import sys

def test_cli():
    """
    Runs the CLI and checks for a successful exit code.
    Simulate argparse input.
    """
    pwncli.main()
    
    # login
    sys.argv=['pwncli', 'login', '-u', 'test1337', '-p', os.environ['TEST_PASSWORD']]
    pwncli.main()
    
    sys.argv=['pwncli', 'get', '--dojos']
    pwncli.main()
    
    sys.argv=['pwncli', 'get', '--dojos', '--modules', 'fundamentals']
    pwncli.main()
    
    sys.argv=['pwncli', 'get', '--dojos', '--modules', 'fundamentals', '--challenges', 'program-misuse']
    pwncli.main()
    
    sys.argv=['pwncli', 'get', '--dojo-ranking', 'fundamentals']
    pwncli.main()
    
    sys.argv=['pwncli', 'get', '--dojo-ranking', 'fundamentals', '--module-ranking', 'program-misuse']
    pwncli.main()
    
    sys.argv=['pwncli', 'get', '--belt', 'blue']
    pwncli.main()
    
    sys.argv=['pwncli', 'get', '--info']
    pwncli.main()
import pwncollege.pwncli as pwncli
import os
import sys

def test_cli():
    """
    Runs the CLI and checks for a successful exit code.
    Simulate argparse input.
    """
    pwncli.main()
    
def test_login():
    sys.argv=['pwncli', 'login', '-u', 'test1339', '-p', os.environ['TEST_PASSWORD']]
    pwncli.main()
    
def test_get():
    sys.argv=['pwncli', 'get', '--dojos']
    pwncli.main()
    
    sys.argv=['pwncli', 'get', '--dojos', '--modules', 'fundamentals']
    pwncli.main()
    
    sys.argv=['pwncli', 'get', '--dojos', '--modules', 'fundamentals', '--challenges', 'talking-web']
    pwncli.main()
    
    sys.argv=['pwncli', 'get', '--dojo-ranking', 'fundamentals']
    pwncli.main()
    
    sys.argv=['pwncli', 'get', '--dojo-ranking', 'fundamentals', '--module-ranking', 'talking-web']
    pwncli.main()
    
    sys.argv=['pwncli', 'get', '--belt', 'blue']
    pwncli.main()
    
    sys.argv=['pwncli', 'get', '--info']
    pwncli.main()
    
def test_challenge():
    sys.argv=['pwncli', 'challenge', '-d', 'fundamentals', '-m', 'talking-web', '-c', 'http-browser', '-r', '-s']
    pwncli.main()
    
    sys.argv=['pwncli', 'challenge', '-d', 'fundamentals', '-m', 'talking-web', '-c', 'http-browser', '-f', '123']
    pwncli.main()
    
    sys.argv=['pwncli', 'challenge', '-d', 'fundamentals', '-m', 'talking-web', '-c', 'http-browser', '-e', 'id']
    pwncli.main()
    
    sys.argv=['pwncli', 'challenge', '-d', 'fundamentals', '-m', 'talking-web', '-c', 'http-browser', '-p']
    pwncli.main()
    
def test_profile():
    sys.argv=['pwncli', 'profile', '-u', 'test1337', '-w', 'example.com']
    pwncli.main()
    
    sys.argv=['pwncli', 'profile', '-u', 'test1339', '-p', os.environ['TEST_PASSWORD'] , '-w', 'test.com']
    pwncli.main()
    
    # sys.argv=['pwncli', 'profile', '-s', 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQD9rhCtGio/xC4vjCBhROS6CQxBoBQGaPAHFA+rtb4llAOPO8XXZnG6U/Rc1+syHvXCJ2z5EwXCz3le8GYcQ5yL9JU5pWjeqEdv4K7/GOStF1EClrIjrv6g028iucPESZ3pPbk8TzepuOgoZORFoIuXIGLZb07loJF9BZ4tSAEWXf/zcI1gDbFjfT+td4ipAlLosLoOl+hvmGvdpQr943Ych7siRwqnNSKTRM62QjPkAk8B7BSOPJ4a2S4aDSwE4FDsdi8tn86h5HhRnLrCUuKm4VcPmGS+LXgggaxkRDI7fBUPtwqtKfIuOenQe5YJMzNgU6ioBHT5JvBBoeunAMUQoVkeU6iy1eiO19q4YKq1pOolBpWd2Bs2tYD83HwxGwmvOqcckCbii1orrohbianhEVpkJhpiP1cZfD2+QteXXcPRgRBupOIukYwKuotrmbJWmK5jzjvF1Z/4ItM3t15icJ1RStNtt8giUt7rPg6T+Wwb6AS+ObY3Pv1AwKPVBQU=']
    # pwncli.main()
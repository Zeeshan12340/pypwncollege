class PwnException(Exception):
    """Base exception class for `pwncollege`"""

    pass


class ApiError(PwnException):
    """The API responded in an unexpected way"""


class AuthenticationException(PwnException):
    """An error authenticating to the API"""

    pass


class NotFoundException(PwnException):
    """The API returned a 404 response for this request"""

    pass


class MissingEmailException(AuthenticationException):
    """An email was not given where it was required"""

    pass


class MissingPasswordException(AuthenticationException):
    """A password was not given where it was required"""

    pass


class ChallengeException(PwnException):
    """An error associated with a challenge"""

    pass


class TooManyRestartAttempts(ChallengeException):
    """Error for too many restart attempts"""

    pass



class SolveError(PwnException):
    """Exceptions for solving"""


class IncorrectFlagException(SolveError):
    """An incorrect flag was submitted"""

    pass


class FlagAlreadySubmitted(SolveError):
    """Player has already completed the flag for this challenge"""

    pass


class IncorrectArgumentException(PwnException):
    """An incorrectly formatted argument was passed"""

    reason: str

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"IncorrectArgumentException(reason='{self.reason}')"

    def __init__(self, reason: str):
        self.reason = reason

    pass


class RateLimitException(PwnException):
    """An internal ratelimit to prevent spam was violated"""

    def __init__(self, message):
        print(message)
        super().__init__(message)

class ServerErrorException(PwnException):
    """A server error occured and an endpoint return a >500 status code"""

    def __init__(self, message):
        print(message)
        super().__init__(message)


class CacheException(PwnException):
    """There was an issue with the token cache"""

    pass

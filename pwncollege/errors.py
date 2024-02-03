class PwnException(Exception):
    """Base exception class for `pwncollege`"""

    pass


class AuthenticationException(PwnException):
    """An error authenticating to the API"""

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

class ServerErrorException(PwnException):
    """A server error occured and an endpoint return a >500 status code"""

    def __init__(self, message):
        print(message)
        super().__init__(message)



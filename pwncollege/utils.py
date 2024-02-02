import requests
import re
from .constants import SITE_BASE

def cookie_expired(token: str) -> bool:
    """Checks if session cookie is expired

    Args:
        token: A UUID session string + random ascii letters
    Returns:
        If the token is expired

    """
    if not token:
        return False
    res = requests.get(SITE_BASE + "/settings", headers={"Cookie": "session=" + token}, allow_redirects=False)
    return res.status_code != 200

def parse_csrf_token(text):
        match = re.search("'csrfNonce': \"(\\w+)\"", text)
        assert match, "Failed to find CSRF token"
        return match.group(1)

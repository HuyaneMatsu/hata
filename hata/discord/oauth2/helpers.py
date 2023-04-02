__all__ = ('parse_oauth2_redirect_url',)

import re


OAUTH2_REQUEST_URL_RP = re.compile('(https?://.+?)\?code=([a-zA-Z0-9]{30})')


def parse_oauth2_redirect_url(url):
    """
    Parses the `redirect_url` and the `code` out from a whole `url`, what an user was redirected to after oauth2
    authorization.
    
    If the parsing was successful, then returns a `tuple` of `redirect_url` and `code`. If it fails, returns `None`.
    
    Parameters
    ----------
    url : `str`
        A whole to url to parse from

    Returns
    -------
    result : `None`, `tuple` (`str`, `str`)
    """
    result = OAUTH2_REQUEST_URL_RP.fullmatch(url)
    if result is None:
        return None
    
    return result.groups()

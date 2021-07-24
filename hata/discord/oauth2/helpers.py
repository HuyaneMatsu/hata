__all__ = ('parse_oauth2_redirect_url',)

import re

DEFAULT_LOCALE = 'en-US'
LOCALES = {DEFAULT_LOCALE: DEFAULT_LOCALE}


def parse_locale(data):
    """
    Gets `'local'`'s value out from the given `dict`. If found returns it, if not, then returns `DEFAULT_LOCAL`.
    
    To not keep using new local values at every case, the already used local values are cached at `LOCALE`.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Some data received from Discord.
    
    Returns
    -------
    locale : `str`
    """
    try:
        locale = data['locale']
    except KeyError:
        return DEFAULT_LOCALE
    
    locale = LOCALES.setdefault(locale, locale)
    return locale


def parse_preferred_locale(data):
    """
    Gets `'preferred_locale'`'s value out from the given `dict`. If found returns it, if not, then returns
    `DEFAULT_LOCAL`.
    
    To not keep using new local values at every case, the already used local values are cached at `LOCALE`.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Some data received from Discord.
    
    Returns
    -------
    locale : `str`
    """
    try:
        locale = data['preferred_locale']
    except KeyError:
        return DEFAULT_LOCALE
    
    locale = LOCALES.setdefault(locale, locale)
    return locale


def parse_locale_optional(data):
    """
    Gets `'local'`'s value out from the given `dict`. If found returns it, if not, then returns `None`.
    
    To not keep using new local values at every case, the already used local values are cached at `LOCALE`.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Some data received from Discord.
    
    Returns
    -------
    locale : `None` or `str`
    """
    try:
        locale = data['locale']
    except KeyError:
        return None
    
    locale = LOCALES.setdefault(locale, locale)
    return locale


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
    result : `None` or `tuple` (`str`, `str`)
    """
    result = OAUTH2_REQUEST_URL_RP.fullmatch(url)
    if result is None:
        return None
    
    return result.groups()


OAUTH2_SCOPES = {v: v for v in ('activities.read', 'activities.write', 'applications.builds.read',
    'applications.builds.upload', 'applications.commands', 'applications.entitlements', 'applications.store.update',
    'bot', 'connections', 'email', 'guilds', 'guilds.join', 'identify', 'messages.read', 'rpc', 'rpc.api',
    'rpc.notifications.read', 'webhook.incoming')}

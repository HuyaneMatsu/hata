__all__ = ('LIBRARY_USER_AGENT',)

from sys import implementation

from scarletio import IgnoreCaseMultiValueDictionary, IgnoreCaseString
from scarletio.web_common.headers import AUTHORIZATION, USER_AGENT

from ... import __version__
from ...env import API_VERSION, LIBRARY_AGENT_APPENDIX, LIBRARY_URL, LIBRARY_VERSION


# to receive
RATE_LIMIT_REMAINING = IgnoreCaseString('X-RateLimit-Remaining')
RATE_LIMIT_RESET = IgnoreCaseString('X-RateLimit-Reset')
RATE_LIMIT_RESET_AFTER = IgnoreCaseString('X-RateLimit-Reset-After')
RATE_LIMIT_LIMIT = IgnoreCaseString('X-RateLimit-Limit')
RATE_LIMIT_HASH = IgnoreCaseString('X-ratelimit-bucket')

# to send
AUDIT_LOG_REASON = IgnoreCaseString('X-Audit-Log-Reason')
RATE_LIMIT_PRECISION = IgnoreCaseString('X-RateLimit-Precision')
DEBUG_OPTIONS = IgnoreCaseString('X-Debug-Options')


# user agent
def build_user_agent(user_agent_base):
    """
    Builds the user agent header to use.
    
    Parameters
    ----------
    user_agent_base : `str`
        The base user agent to use.
    
    Returns
    -------
    user_agent : `str`
    """
    parts = []
    parts.append(user_agent_base)
    parts.append(' ')
    
    if LIBRARY_AGENT_APPENDIX is None:
        parts.append('Python (')
        parts.append(implementation.name)
        parts.append(' ')
        
        version = implementation.version
        parts.append(str(version[0]))
        parts.append('.')
        parts.append(str(version[1]))
        
        release_level = version[3]
        if release_level != 'final':
            parts.append(' ')
            parts.append(release_level)
        
        parts.append(')')
    
    else:
        parts.append(LIBRARY_AGENT_APPENDIX)
    
    return ''.join(parts)


# to send (generated)
if LIBRARY_VERSION is None:
    LIBRARY_VERSION = __version__

LIBRARY_USER_AGENT_BASE = f'DiscordBot ({LIBRARY_URL}, {LIBRARY_VERSION})'
LIBRARY_USER_AGENT = build_user_agent(LIBRARY_USER_AGENT_BASE)


# header building
def build_headers(bot, token, debug_options):
    """
    Builds the headers passed to discord.
    
    Parameters
    ----------
    bot : `bool`
        Whether the respective client is a bot.
    token : `str`
        The client's token.
    debug_options: `None | set<str>`
        Http debug options.
    
    Returns
    -------
    headers : ``IgnoreCaseMultiValueDictionary``
    """
    headers = IgnoreCaseMultiValueDictionary()
    headers[USER_AGENT] = LIBRARY_USER_AGENT
    headers[AUTHORIZATION] = f'Bot {token!s}' if bot else token
    
    if API_VERSION in (6, 7):
        headers[RATE_LIMIT_PRECISION] = 'millisecond'
    
    if (debug_options is not None):
        for debug_option in sorted(debug_options):
            headers[DEBUG_OPTIONS] = debug_option
    
    return headers

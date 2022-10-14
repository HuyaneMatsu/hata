__all__ = ('parse_oauth2_redirect_url',)

import re

from .preinstanced import Oauth2Scope


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


def parse_joined_oauth2_scopes(joined_scopes):
    """
    Parses the joined oauth2 scopes.
    
    Parameters
    ----------
    joined_scopes : `str`
        The joined scopes.
    
    Returns
    -------
    scopes : `None`, `tuple` of ``Oauth2Scope``
    """
    split_scopes = joined_scopes.split()
    if not split_scopes:
        return None
    
    split_scopes.sort()
    
    return tuple(Oauth2Scope.get(scope) for scope in split_scopes)


def parse_oauth2_scope_array(scope_array):
    """
    Parsers the given oauth2 scope array.
    
    Parameters
    ----------
    scope_array : `None`, `list` of `str`
        Scope array.
    
    
    Returns
    -------
    scopes : `None`, `tuple` of ``Oauth2Scope``
    """
    if (scope_array is None) or (not scope_array):
        return None
    
    scope_array.sort()
    
    return tuple(Oauth2Scope.get(scope) for scope in scope_array)


def join_oauth2_scopes(scopes):
    """
    Joins the given oauth2 scopes together.
    
    Parameters
    ----------
    scopes : `None`, `tuple` of ``Oauth2Scope``
        Oauth2 scopes to join.
    
    Returns
    -------
    joined_scopes : `str`
    """
    if scopes is None:
        return ''
    
    return ' '.join([scope.value for scope in scopes])


def make_oauth2_scope_array(scopes):
    """
    Converts the given oath2 scopes into a string array.
    
    Parameters
    ----------
    scopes : `None`, `tuple` of ``Oauth2Scope``
        Oauth2 scopes to use.
    
    Returns
    -------
    scope_array : `list` of `str`
    """
    if scopes is None:
        scope_array = []
    else:
        scope_array = [scope.value for scope in scopes]
    
    return scope_array


def _get_one_scope_value(scope):
    """
    Gets the value of one scope.
    
    Used by ``build_joined_scopes``.
    
    Returns
    -------
    scope_value : `str`
    
    Raises
    ------
    TypeError
        - If `scope` is neither ``Oauth2Scope``, `str`.
    """
    if isinstance(scope, Oauth2Scope):
        scope_value =  scope.value
    
    elif isinstance(scope, str):
        scope_value = scope
    
    else:
        raise TypeError(
            f'A scope can be `{Oauth2Scope.__name__}`, `str`; got {scope.__class__.__name__}; {scope!r}.'
        )
    
    return scope_value


def build_joined_scopes(scopes):
    """
    Builds joined scopes from the given value.
    
    Parameters
    ----------
    scopes : ``Oauth2Scope``, `str`, `iterable` of (``Oauth2Scope``, `str`)
        The scopes to join.
    
    Returns
    -------
    joined_scopes : `str`
    
    Raises
    ------
    TypeError
        - If `scopes`'s type is incorrect.
    """
    if isinstance(scopes, Oauth2Scope):
        joined_scopes = scopes.value
    
    elif isinstance(scopes, str):
        joined_scopes = scopes
    
    elif getattr(scopes, '__iter__', None) is not None:
        joined_scopes = ' '.join([_get_one_scope_value(scope) for scope in scopes])
    
    else:
        raise TypeError(
            f'`scopes` can be `str`, `{Oauth2Scope.__name__}`, `iterable` of them; '
            f'got {scopes.__class__.__name__}; {scopes!r}.'
        )
    
    return joined_scopes

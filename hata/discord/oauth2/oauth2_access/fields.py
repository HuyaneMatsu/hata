__all__ = ()

from ...field_parsers import force_string_parser_factory, int_parser_factory
from ...field_putters import force_string_putter_factory, int_putter_factory
from ...field_validators import (
    force_date_time_validator_factory, force_string_validator_factory, int_conditional_validator_factory,
    preinstanced_array_validator_factory, url_required_validator_factory
)

from .preinstanced import Oauth2Scope

# access_token

parse_access_token = force_string_parser_factory('access_token')
put_access_token_into = force_string_putter_factory('access_token')
validate_access_token = force_string_validator_factory('access_token', 0, 1024)

# created_at

validate_created_at = force_date_time_validator_factory('created_at')

# expires_after

parse_expires_after = int_parser_factory('expires_in', 0)
put_expires_after_into = int_putter_factory('expires_in')
validate_expires_after = int_conditional_validator_factory(
    'expires_after',
    0,
    lambda expires_after : expires_after >= 0,
    '>= 0',
)

# refresh_token

parse_refresh_token = force_string_parser_factory('refresh_token')
put_refresh_token_into = force_string_putter_factory('refresh_token')
validate_refresh_token = force_string_validator_factory('refresh_token', 0, 1024)

# redirect_url

validate_redirect_url = url_required_validator_factory('redirect_url')

# scopes

def parse_scopes(data):
    """
    Parses the oauth2 scopes from the given data.
    
    Parameters
    ----------
    joined_scopes : `str`
        The joined scopes.
    
    Returns
    -------
    scopes : `None`, `tuple` of ``Oauth2Scope``
    """
    joined_scopes = data.get('scope', None)
    if joined_scopes is None:
        return None
    
    split_scopes = joined_scopes.split()
    if not split_scopes:
        return None
    
    split_scopes.sort()
    
    return tuple(Oauth2Scope.get(scope) for scope in split_scopes)


def put_scopes_into(scopes, data, defaults):
    """
    Puts the given oauth2 scopes into a json serializable dictionary.
    
    Parameters
    ----------
    activity_id : `int`
        Activity's identifier.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    if scopes is None:
        joined_scopes = ''
    else:
        joined_scopes = ' '.join([scope.value for scope in scopes])
        
    data['scope'] = joined_scopes
    return data

validate_scopes = preinstanced_array_validator_factory('scopes', Oauth2Scope)

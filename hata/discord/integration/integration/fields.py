__all__ = ()

from ...field_parsers import (
    bool_parser_factory, default_entity_parser_factory, force_string_parser_factory, preinstanced_array_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, default_entity_putter_factory, force_string_putter_factory,
    preinstanced_array_putter_factory
)
from ...field_validators import (
    bool_validator_factory, default_entity_validator, force_string_validator_factory,
    preinstanced_array_validator_factory
)
from ...oauth2 import Oauth2Scope
from ...preconverters import preconvert_preinstanced_type
from ...user import ClientUserBase, User, ZEROUSER

from .constants import  NAME_LENGTH_MAX, NAME_LENGTH_MIN
from .preinstanced import IntegrationType


# enabled

parse_enabled = bool_parser_factory('enabled', True)
put_enabled_into = bool_optional_putter_factory('enabled', True)
validate_enabled = bool_validator_factory('enabled')

# name

parse_name = force_string_parser_factory('name')
put_name_into = force_string_putter_factory('name')
validate_name = force_string_validator_factory('name', NAME_LENGTH_MIN, NAME_LENGTH_MAX)

# scopes

parse_scopes = preinstanced_array_parser_factory('scopes', Oauth2Scope)
put_scopes_into = preinstanced_array_putter_factory('scopes')
validate_scopes = preinstanced_array_validator_factory('scopes', Oauth2Scope)

# type

def parse_type(data):
    """
    Parses out an integration's type the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Entity data.
    
    Returns
    -------
    preinstanced : ``IntegrationType``
    """
    try:
        value = data['type']
    except KeyError:
        preinstanced = IntegrationType.none
    else:
        preinstanced = IntegrationType.get(value)
    
    return preinstanced


def put_type_into(preinstanced, data, defaults):
    """
    Puts the integration type the given `data` json serializable object.
    
    Parameters
    ----------
    preinstanced : ``IntegrationType``
        An integration's type.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    data['type'] = preinstanced.value
    
    return data


def validate_type(preinstanced):
    """
    Validates the given integration type.
    
    Parameters
    ----------
    preinstanced : `None`, ``IntegrationType``, `str`
        An integration's type.
    
    Returns
    -------
    preinstanced : ``IntegrationType``
    
    Raises
    ------
    TypeError
        - If `preinstanced`'s type is incorrect.
    """
    if preinstanced is None:
        return IntegrationType.none
    
    return preconvert_preinstanced_type(preinstanced, 'type', IntegrationType)

# user

parse_user = default_entity_parser_factory('user', User, ZEROUSER)
put_user_into = default_entity_putter_factory('user', ClientUserBase, ZEROUSER)
validate_user = default_entity_validator('user', ClientUserBase, ZEROUSER)

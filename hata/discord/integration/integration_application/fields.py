__all__ = ()

from ...field_parsers import entity_id_parser_factory, force_string_parser_factory, nullable_string_parser_factory
from ...field_putters import entity_id_putter_factory, force_string_putter_factory, nullable_string_putter_factory
from ...field_validators import (
    entity_id_validator_factory, force_string_validator_factory, nullable_string_validator_factory
)
from ...user import ClientUserBase, User, ZEROUSER

from .constants import DESCRIPTION_LENGTH_MAX, DESCRIPTION_LENGTH_MIN, NAME_LENGTH_MAX, NAME_LENGTH_MIN

# bot

def parse_bot(data):
    """
    Parses the integration application's bot from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Integration application data.
    
    Returns
    -------
    bot : ``ClientUserBase``
    """
    user_data = data.get('bot', None)
    if user_data is None:
        bot = ZEROUSER
    else:
        bot = User.from_data(user_data)
    
    return bot


def put_bot_into(user, data, defaults, *, include_internals = False):
    """
    Puts the `bot`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The integration application's bot.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    include_internals : `bool` = `False`, Optional (Keyword only)
        Whether internal fields should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if defaults or (user is not ZEROUSER):
        if user is ZEROUSER:
            user_data = None
        
        else:
            # User not implements `defaults` and `include_internals` for now, so we wont forward them.
            user_data = user.to_data(defaults = defaults, include_internals = include_internals)
        
        data['bot'] = user_data
    
    return data        


def validate_bot(value):
    """
    Validates whether the given value is an application integration bot.
    
    Parameters
    ----------
    value : `None`, ``ClientUserBase``
        The integration application bot.
    
    Returns
    -------
    bot : ``ClientUserBase``
    
    Raises
    ------
    TypeError
        - If `value` is not ``ClientUserBase``.
    """
    if value is None:
        bot = ZEROUSER
    
    elif isinstance(value, ClientUserBase):
        bot = value
    
    else:
        raise TypeError(
            f'`bot` can be `None`, `{ClientUserBase.__name__}`, got {value.__class__.__name__}; {value!r}.'
        )
    
    return bot

# description

parse_description = nullable_string_parser_factory('description')
put_description_into = nullable_string_putter_factory('description')
validate_description = nullable_string_validator_factory('description', DESCRIPTION_LENGTH_MIN, DESCRIPTION_LENGTH_MAX)

# id

parse_id = entity_id_parser_factory('id')
put_id_into = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('integration_application_id')

# name

parse_name = force_string_parser_factory('name')
put_name_into = force_string_putter_factory('name')
validate_name = force_string_validator_factory('name', NAME_LENGTH_MIN, NAME_LENGTH_MAX)

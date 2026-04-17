__all__ = ()

from ...field_parsers import default_date_time_parser_factory, nullable_entity_parser_factory
from ...field_putters import force_date_time_putter_factory
from ...field_validators import force_date_time_validator_factory, nullable_entity_validator_factory
from ...utils import DISCORD_EPOCH_START

from ..message import Message


# message

parse_message = nullable_entity_parser_factory('message', Message)

def put_message(message, data, defaults):
    """
    Puts the given `message` into the given data.
    
    Parameters
    ----------
    message : ``None | Message``
        The message to put into the given `data`.
    
    data : `dict<str, object>`
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default fields should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if defaults or (message is not None):
        if message is None:
            entity_data = None
        else:
            entity_data = message.to_data(defaults = defaults, include_internals = True)
        
        data['message'] = entity_data
    
    return data

validate_message = nullable_entity_validator_factory('message', Message)


# pinned_at

parse_pinned_at = default_date_time_parser_factory('pinned_at', DISCORD_EPOCH_START)
put_pinned_at = force_date_time_putter_factory('pinned_at')
validate_pinned_at = force_date_time_validator_factory('pinned_at')

__all__ = ()

from math import ceil

from ...channel import Channel
from ...field_parsers import entity_id_parser_factory, int_parser_factory
from ...field_putters import entity_id_optional_putter_factory, int_putter_factory
from ...field_validators import entity_id_validator_factory

from .constants import AUTO_MODERATION_ACTION_TIMEOUT_MAX

# channel_id

parse_channel_id = entity_id_parser_factory('channel_id')
put_channel_id_into = entity_id_optional_putter_factory('channel_id')
validate_channel_id = entity_id_validator_factory('channel_id', Channel)

# duration

parse_duration = int_parser_factory('duration_seconds', 0)
put_duration_into = int_putter_factory('duration_seconds')

def validate_duration(duration):
    """
    Validates the given duration.
    
    Parameters
    ----------
    duration : `None`, `int`, `float`
        The timeout's duration applied on trigger.
    
    Returns
    -------
    duration : `int`
    
    Raises
    ------
    TypeError
        - If `duration` type is incorrect.
    """
    if duration is None:
        duration = 0
    
    elif isinstance(duration, int):
        pass
    
    elif isinstance(duration, float):
        duration = ceil(duration)
    
    else:
        raise TypeError(
            f'`duration` can be `None`, `int`, `float`, got {duration.__class__.__name__}; {duration!r}.'
        )
    
    if duration < 0:
        duration = 0
    
    elif duration > AUTO_MODERATION_ACTION_TIMEOUT_MAX:
        duration = AUTO_MODERATION_ACTION_TIMEOUT_MAX
    
    return duration

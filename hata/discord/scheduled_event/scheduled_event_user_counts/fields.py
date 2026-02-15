__all__ = ()

from datetime import datetime as DateTime

from ...field_parsers import int_parser_factory
from ...field_putters import int_putter_factory
from ...field_validators import int_conditional_validator_factory
from ...utils import datetime_to_id, id_to_datetime


# count

parse_count = int_parser_factory('guild_scheduled_event_count', 0)
put_count = int_putter_factory('guild_scheduled_event_count')
validate_count = int_conditional_validator_factory(
    'count',
    0,
    (lambda count : count >= 0),
    '>= 0',
)


# count_by_occasion_overwrite


def parse_occasion_counts(data):
    """
    Parses occasion counts from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    occasion_counts : `None | dict<DateTime, int>`
    """
    count_by_occasion_overwrite_data = data.get('guild_scheduled_event_exception_counts', None)
    if (count_by_occasion_overwrite_data is None) or (not count_by_occasion_overwrite_data):
        return None
    
    return {id_to_datetime(int(key)) : value for key, value in count_by_occasion_overwrite_data.items()}


def put_occasion_counts(occasion_counts, data, defaults):
    """
    Serialises occasion counts into the given data
    
    Parameters
    ----------
    occasion_counts : `None | dict<DateTime, int>`
        Occasion counts to serialise.
    
    data : `dict<str, object>`
        Reaction event data.
    
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    data['guild_scheduled_event_exception_counts'] = (
        {} if occasion_counts is None else {str(datetime_to_id(key)): value for key, value in occasion_counts.items()}
    )
    return data


def validate_occasion_counts(occasion_counts):
    """
    Validates the given occasion counts value.
    
    Parameters
    ----------
    occasion_counts : `object`
        Occasion counts to validate.
    
    Returns
    -------
    occasion_counts_validated : `None | dict<DateTime, int>`
    
    Raises
    ------
    TypeError
        - Value of invalid type given.
    """
    if occasion_counts is None:
        return None
    
    if isinstance(occasion_counts, dict):
        occasion_counts_validated = None
        
        for key, value in occasion_counts.items():
            if not isinstance(key, DateTime):
                raise TypeError(
                    f'`occasion_counts` keys can be `DateTime`, got {type(key).__name__}; {key!r}; '
                    f'occasion_counts = {occasion_counts!r}.'
                )
            
            if not isinstance(value, int):
                raise TypeError(
                    f'`occasion_counts` values can be `int`, got {type(key).__name__}; {key!r}; '
                    f'occasion_counts = {occasion_counts!r}.'
                )
            
            if occasion_counts_validated is None:
                occasion_counts_validated = {}
            
            occasion_counts_validated[key] = value
        
        return occasion_counts_validated
    
    # No other case needed.
    raise TypeError(
        f'`occasion_counts` can be `None` or `dict`, got {type(occasion_counts).__name__}; {occasion_counts!r}.'
    )

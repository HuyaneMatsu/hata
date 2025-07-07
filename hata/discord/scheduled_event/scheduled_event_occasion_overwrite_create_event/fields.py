__all__ = ()

from ...field_parsers import entity_id_parser_factory
from ...field_putters import entity_id_optional_putter_factory, entity_id_putter_factory
from ...field_validators import entity_id_validator_factory, entity_validator_factory

from ..scheduled_event import ScheduledEvent
from ..scheduled_event_occasion_overwrite import ScheduledEventOccasionOverwrite


# guild_id

parse_guild_id = entity_id_parser_factory('guild_id')
put_guild_id = entity_id_optional_putter_factory('guild_id')
validate_guild_id = entity_id_validator_factory('guild_id', NotImplemented, include = 'Guild')


# scheduled_event_id

parse_scheduled_event_id = entity_id_parser_factory('event_id')
put_scheduled_event_id = entity_id_putter_factory('event_id')
validate_scheduled_event_id = entity_id_validator_factory('scheduled_event_id', ScheduledEvent)


# occasion_overwrite

def parse_occasion_overwrite(data):
    """
    Parses an occasion overwrite out from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    occasion_overwrite : ``ScheduledEventOccasionOverwrite``
    """
    return ScheduledEventOccasionOverwrite.from_data(data)


def put_occasion_overwrite(occasion_overwrite, data, defaults):
    """
    Serializes the given scheduled event occasion overwrite.
    
    Parameters
    ----------
    occasion_overwrite : ``ScheduledEventOccasionOverwrite``
        Occasion overwrite to serialize.
    
    data : `dict<str, object>`
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    data.update(occasion_overwrite.to_data(defaults = defaults, include_internals = True))
    return data


validate_occasion_overwrite = entity_validator_factory('occasion_overwrite', ScheduledEventOccasionOverwrite)

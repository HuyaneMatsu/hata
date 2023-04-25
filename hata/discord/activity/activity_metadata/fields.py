__all__ = ()

from ...field_parsers import (
    entity_id_parser_factory, flag_parser_factory, force_string_parser_factory, nullable_entity_parser_factory,
    nullable_functional_parser_factory, nullable_string_parser_factory
)
from ...field_putters import (
    entity_id_optional_putter_factory, flag_optional_putter_factory, force_string_putter_factory,
    nullable_entity_optional_putter_factory, nullable_functional_optional_putter_factory,
    nullable_string_optional_putter_factory, url_optional_putter_factory
)
from ...field_validators import (
    entity_id_validator_factory, flag_validator_factory, force_string_validator_factory,
    nullable_date_time_validator_factory, nullable_entity_validator_factory, nullable_string_validator_factory,
    url_optional_validator_factory
)
from ...utils import datetime_to_millisecond_unix_time, millisecond_unix_time_to_datetime

from ..activity_assets import ActivityAssets
from ..activity_party import ActivityParty
from ..activity_secrets import ActivitySecrets
from ..activity_timestamps import ActivityTimestamps

from .flags import ActivityFlag

# application_id

parse_application_id = entity_id_parser_factory('application_id')
put_application_id_into = entity_id_optional_putter_factory('application_id')
validate_application_id = entity_id_validator_factory('application_id', NotImplemented, include = 'Application')

# assets

parse_assets = nullable_entity_parser_factory('assets', ActivityAssets)
put_assets_into = nullable_entity_optional_putter_factory('assets', ActivityAssets)
validate_assets = nullable_entity_validator_factory('assets', ActivityAssets)

# created_at

def parse_created_at(data):
    """
    Parses when the activity was created from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Activity timestamp data.
    
    Returns
    -------
    created_at : `None`, `datetime`
    """
    created_at = data.get('created_at', None)
    if (created_at is not None):
        return millisecond_unix_time_to_datetime(created_at)


def put_created_at_into(created_at, data, defaults):
    """
    Puts the activity created at timestamp into the given data.
    
    Parameters
    ----------
    created_at : `None`, `datetime`
        Activity timestamps created_at.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    if defaults or (created_at is not None):
        if (created_at is not None):
            created_at = datetime_to_millisecond_unix_time(created_at)
        
        data['created_at'] = created_at
    
    return data


validate_created_at = nullable_date_time_validator_factory('created_at')

# details

parse_details = nullable_string_parser_factory('details')
put_details_into = nullable_string_optional_putter_factory('details')
validate_details = nullable_string_validator_factory('details', 0, 1024)

# emoji

parse_emoji = nullable_functional_parser_factory('emoji', NotImplemented, include = 'create_partial_emoji_from_data')
put_emoji_into = nullable_functional_optional_putter_factory(
    'emoji', NotImplemented, include = 'create_partial_emoji_data'
)
validate_emoji = nullable_entity_validator_factory('emoji', NotImplemented, include = 'Emoji')

# flags

parse_flags = flag_parser_factory('flags', ActivityFlag)
put_flags_into = flag_optional_putter_factory('flags', ActivityFlag())
validate_flags = flag_validator_factory('flags', ActivityFlag)

# id


def parse_id(data):
    """
    Parses out activity identifier from the given data
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Activity data.
    
    Returns
    -------
    activity_id : `int`
    """
    activity_id = data.get('id', None)
    if (activity_id is None):
        return 0
    
    try:
        return int(activity_id, base = 16)
    except ValueError:
        # Some activity types have `custom` id-s, at those cases we default back to `0`.
        return 0


def put_id_into(activity_id, data, defaults):
    """
    Puts the given activity identifier into a json serializable dictionary.
    
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
    if activity_id:
        data['id'] = format(activity_id, 'x')
    
    return data


validate_id = entity_id_validator_factory('activity_id')

# name

parse_name = force_string_parser_factory('name')
put_name_into = force_string_putter_factory('name')
validate_name = force_string_validator_factory('name', 0, 1024)

# party

parse_party = nullable_entity_parser_factory('party', ActivityParty)
put_party_into = nullable_entity_optional_putter_factory('party', ActivityParty)
validate_party = nullable_entity_validator_factory('party', ActivityParty)

# secrets

parse_secrets = nullable_entity_parser_factory('secrets', ActivitySecrets)
put_secrets_into = nullable_entity_optional_putter_factory('secrets', ActivitySecrets)
validate_secrets = nullable_entity_validator_factory('secrets', ActivitySecrets)

# session_id

parse_session_id = nullable_string_parser_factory('session_id')
put_session_id_into = nullable_string_optional_putter_factory('session_id')
validate_session_id = nullable_string_validator_factory('session_id', 0, 1024)

# state

parse_state = nullable_string_parser_factory('state')
put_state_into = nullable_string_optional_putter_factory('state')
validate_state = nullable_string_validator_factory('state', 0, 1024)

# sync_id

parse_sync_id = nullable_string_parser_factory('sync_id')
put_sync_id_into = nullable_string_optional_putter_factory('sync_id')
validate_sync_id = nullable_string_validator_factory('sync_id', 0, 1024)

# timestamps

parse_timestamps = nullable_entity_parser_factory('timestamps', ActivityTimestamps)
put_timestamps_into = nullable_entity_optional_putter_factory('timestamps', ActivityTimestamps)
validate_timestamps = nullable_entity_validator_factory('timestamps', ActivityTimestamps)

# url

parse_url = nullable_string_parser_factory('url')
put_url_into = url_optional_putter_factory('url')
validate_url = url_optional_validator_factory('url')

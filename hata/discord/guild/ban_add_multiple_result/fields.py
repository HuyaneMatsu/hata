__all__ = ()

from ...field_parsers import entity_id_array_parser_factory
from ...field_putters import nullable_entity_id_array_putter_factory, int_optional_putter_factory
from ...field_validators import (
    entity_id_array_validator_factory, entity_id_set_validator_factory, int_conditional_validator_factory
)
from ...user import ClientUserBase

from .constants import DELETE_MESSAGE_DURATION_DEFAULT, DELETE_MESSAGE_DURATION_MIN, DELETE_MESSAGE_DURATION_MAX

# banned_user_ids

parse_banned_user_ids = entity_id_array_parser_factory('banned_users')
put_banned_user_ids_into = nullable_entity_id_array_putter_factory('banned_users')
validate_banned_user_ids = entity_id_array_validator_factory('banned_user_ids', ClientUserBase)

# delete_message_duration

put_delete_message_duration_into = int_optional_putter_factory(
    'delete_message_seconds', DELETE_MESSAGE_DURATION_DEFAULT
)

validate_delete_message_duration = int_conditional_validator_factory(
    'delete_message_duration',
    DELETE_MESSAGE_DURATION_DEFAULT,
    (
        lambda delete_message_duration :
            delete_message_duration >= DELETE_MESSAGE_DURATION_MIN and
            delete_message_duration <= DELETE_MESSAGE_DURATION_MAX
    ),
    f'>= {DELETE_MESSAGE_DURATION_MIN!r} and <= {DELETE_MESSAGE_DURATION_MAX!r}',
)


# failed_user_ids

parse_failed_user_ids = entity_id_array_parser_factory('failed_users')
put_failed_user_ids_into = nullable_entity_id_array_putter_factory('failed_users')
validate_failed_user_ids = entity_id_array_validator_factory('failed_user_ids', ClientUserBase)

# user_ids

def put_user_ids_into(user_ids, data, defaults):
    """
    Puts the user identifiers into the given data.
    
    Parameters
    ----------
    user_ids : `set<int>`
        The user identifiers to put into the given data.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    data['user_ids'] = [str(user_id) for user_id in user_ids]
    return data


validate_user_ids = entity_id_set_validator_factory('user_ids', ClientUserBase)


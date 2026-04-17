__all__ = ()

from ...field_parsers import (
    int_parser_factory, nullable_date_time_parser_factory, nullable_string_parser_factory, preinstanced_parser_factory
)
from ...field_putters import (
    int_putter_factory, nullable_date_time_optional_putter_factory, nullable_string_optional_putter_factory,
    preinstanced_putter_factory
)
from ...field_validators import (
    int_conditional_validator_factory, nullable_date_time_validator_factory, nullable_string_validator_factory,
    preinstanced_validator_factory
)

from .preinstanced import InviteAllowedUserIdsStatusStatus


# completed_at

parse_completed_at = nullable_date_time_parser_factory('completed_at')
put_completed_at = nullable_date_time_optional_putter_factory('completed_at')
validate_completed_at = nullable_date_time_validator_factory('completed_at')


# error_message

parse_error_message = nullable_string_parser_factory('error_message')


def put_error_message(error_message, data, defaults):
    """
    Puts the given `error_message` into the given `data` json serializable object.
    
    Parameters
    ----------
    field_value : `None | str`
        String field value.
    
    data : `dict<str, object>`
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default values as their defaults should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    data['error_message'] = error_message
    return data


validate_error_message = nullable_string_validator_factory('error_message', 0, 1024)


# processed

parse_processed = int_parser_factory('processed_users', 0)
put_processed = int_putter_factory('processed_users')
validate_processed = int_conditional_validator_factory(
    'processed',
    0,
    (lambda processed : processed >= 0),
    '>= 0',
)


# started_at

parse_started_at = nullable_date_time_parser_factory('created_at')
put_started_at = nullable_date_time_optional_putter_factory('created_at')
validate_started_at = nullable_date_time_validator_factory('started_at')


# status

parse_status = preinstanced_parser_factory(
    'status', InviteAllowedUserIdsStatusStatus, InviteAllowedUserIdsStatusStatus.none
)
put_status = preinstanced_putter_factory('status')
validate_status = preinstanced_validator_factory('status', InviteAllowedUserIdsStatusStatus)


# total

parse_total = int_parser_factory('total_users', 0)
put_total = int_putter_factory('total_users')
validate_total = int_conditional_validator_factory(
    'total',
    0,
    (lambda total : total >= 0),
    '>= 0',
)

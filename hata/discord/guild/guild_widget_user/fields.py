__all__ = ()

from ...field_parsers import force_string_parser_factory
from ...field_putters import url_optional_putter_factory
from ...field_validators import (
    int_conditional_validator_factory, nullable_string_validator_factory, url_required_validator_factory
)
from ...user.user.fields import (
    parse_discriminator, parse_id, parse_name, parse_status, put_discriminator, put_id, put_name,
    put_status, validate_discriminator, validate_name, validate_status
)


# activity_name

def parse_activity_name(data):
    """
    Parses out the `activity_name` field from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Guild widget user data.
    
    Returns
    -------
    activity_name : `None`, `str`
    """
    activity_data = data.get('game', None)
    if activity_data is None:
        activity_name = None
    else:
        activity_name = activity_data.get('name', None)
        if (activity_name is not None) and (not activity_name):
            activity_name = None
    
    return activity_name


def put_activity_name(activity_name, data, defaults):
    """
    Puts the given activity name into a json serializable dictionary.
    
    Parameters
    ----------
    activity_name : `str`
        Activity's name.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if (activity_name is not None) or defaults:
        if activity_name is None:
            activity_name = ''
        data['game'] = {'name': activity_name}
    
    return data


validate_activity_name = nullable_string_validator_factory('activity_name', 0, 1024)

# id

validate_id = int_conditional_validator_factory(
    'id',
    0,
    lambda id : id >= 0 and id <= 99,
    '>= 0 and <= 99',
)

# url

parse_avatar_url = force_string_parser_factory('avatar_url')
put_avatar_url = url_optional_putter_factory('avatar_url')
validate_avatar_url = url_required_validator_factory('avatar_url')

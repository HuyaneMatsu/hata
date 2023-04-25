__all__ = ()

from ...activity import Activity
from ...channel import Channel
from ...field_parsers import default_entity_parser_factory, entity_id_parser_factory
from ...field_putters import entity_id_optional_putter_factory, entity_id_putter_factory
from ...field_validators import default_entity_validator, entity_id_set_validator_factory, entity_id_validator_factory
from ...user import ClientUserBase

from .constants import ACTIVITY_KEY

# activity

parse_activity = default_entity_parser_factory(ACTIVITY_KEY, Activity, default_factory = lambda : Activity())


def put_activity_into(activity, data, defaults):
    """
    Puts the activity into the given data.
    
    Parameters
    ----------
    activity : ``Activity``
        The activity to put into the given data.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    data[ACTIVITY_KEY] = activity.to_data(include_internals = True, user = True)
    return data


validate_activity = default_entity_validator('activity', Activity, default_factory = lambda : Activity())

# application_id

def parse_application_id(data):
    """
    Parses application identifier from the given embedded activity state data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Embedded activity state data.
    
    Returns
    -------
    application_application_id : `int`
    """
    activity_data = data.get(ACTIVITY_KEY, None)
    if activity_data is None:
        return 0
    
    application_id = activity_data.get('application_id', None)
    if application_id is None:
        return 0
    
    return int(application_id)


def put_application_id_into(application_id, data, defaults):
    """
    Puts the application identifier into the given data.
    
    Parameters
    ----------
    application_id : `int`
        The represented application's identifier.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    if application_id or defaults:
        activity_data = data.get(ACTIVITY_KEY, None)
        if activity_data is None:
            activity_data = {}
            data[ACTIVITY_KEY] = activity_data
        
        if application_id:
            application_id = str(application_id)
        else:
            application_id = None
        
        activity_data['application_id'] = application_id
        
    return data


validate_application_id = entity_id_validator_factory('application_id', NotImplemented, include = 'Application')

# channel_id

parse_channel_id = entity_id_parser_factory('channel_id')
put_channel_id_into = entity_id_putter_factory('channel_id')
validate_channel_id = entity_id_validator_factory('channel_id', Channel)

# guild_id

parse_guild_id = entity_id_parser_factory('guild_id')
put_guild_id_into = entity_id_optional_putter_factory('guild_id')
validate_guild_id = entity_id_validator_factory('guild_id', NotImplemented, include = 'Guild')

# user_ids

def parse_user_ids(data):
    """
    Parses the user identifiers from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Embedded activity state data.
    
    Returns
    -------
    user_ids : `set` of `int`
    """
    user_ids = data.get('users', None)
    if user_ids is None:
        return set()
    
    return {int(user_id) for user_id in user_ids}


def put_user_ids_into(user_ids, data, defaults):
    """
    Puts the user identifiers into the given data.
    
    Parameters
    ----------
    user_ids : `set` of `int`
        The user identifiers to put into the given data.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    data['users'] = [str(user_id) for user_id in user_ids]
    return data


validate_user_ids = entity_id_set_validator_factory('user_ids', ClientUserBase)

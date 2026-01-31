__all__ = ()

from ...channel import Channel
from ...field_parsers import bool_parser_factory, int_parser_factory
from ...field_putters import bool_optional_putter_factory, int_putter_factory
from ...field_validators import (
    bool_validator_factory, int_conditional_validator_factory, nullable_entity_array_validator_factory,
    nullable_object_array_validator_factory
)
from ...user import create_partial_user_from_id, thread_user_create

from ..message import Message


def parse_analytics_id(data):
    """
    Parses analytics identifier from teh given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    analytics_id : `int`
    """
    analytics_id = data.get('analytics_id', None)
    if (analytics_id is not None):
        try:
            return int(analytics_id, 16)
        except ValueError:
            pass
    
    return 0


def put_analytics_id(analytics_id, data, defaults):
    """
    Serialises the given analytics identifier.
    
    Parameters
    ----------
    analytics_id : `int`
        The value to serialise.
    
    data : `dict<str, object>`
        Data to serialise into.
    
    defaults : `bool`
        Whether fields as their defaults should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    data['analytics_id'] = format(analytics_id, '0>32x')
    return data


def validate_analytics_id(analytics_id):
    """
    Whether the given `analytics_id` value.
    
    Parameters
    ----------
    analytics_id : `None | int`
        The value to validate.
    
    Returns
    -------
    analytics_id : `int`
    
    Raises
    ------
    TypeError
        - If the given value's type is incorrect.
    ValueError
        - if the given value's value is out of bounds.
    """
    if analytics_id is None:
        return 0
    
    if not isinstance(analytics_id, int):
        raise TypeError(f'`analytics_id` can be `None`, | `int`, got {type(analytics_id).__name__}; {analytics_id!r}.')
    
    if analytics_id < 0:
        raise ValueError(f'`analytics_id` cannot be <= 0, got {analytics_id!r}.')
    
    if analytics_id > (1 << 128) - 1:
        raise ValueError(f'`analytics_id` can be up to 128 bit long; got {analytics_id!r}.')
    
    return analytics_id


# deep_historical_indexing_in_progress

parse_deep_historical_indexing_in_progress = bool_parser_factory('doing_deep_historical_index', False)
put_deep_historical_indexing_in_progress = bool_optional_putter_factory('doing_deep_historical_index', False)
validate_deep_historical_indexing_in_progress = bool_validator_factory('doing_deep_historical_index', False)


# messages


def parse_messages(data):
    """
    Parses the messages out from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    messages : ``None | tuple<Message>``
    """
    message_datas = data.get('messages', None)
    if (message_datas is None) or (not message_datas):
        messages = None
    else:
        messages = (*(Message.from_data(message_data[0]) for message_data in message_datas),)
    
    return messages


def put_messages(messages, data, defaults):
    """
    Serialises the given messages.
    
    Parameters
    ----------
    messages : ``None | tuple<Message>``
        The value to serialise.
    
    data : `dict<str, object>`
        Data to serialise into.
    
    defaults : `bool`
        Whether fields as their default should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if messages is None:
        message_datas = []
    else:
        message_datas = [[message.to_data(defaults = defaults, include_internals = True)] for message in messages]
    
    data['messages'] = message_datas
    return data


validate_messages = nullable_object_array_validator_factory('messages', Message)


# result_count

parse_result_count = int_parser_factory('total_results', 0)
put_result_count = int_putter_factory('total_results')
validate_result_count = int_conditional_validator_factory(
    'result_count',
    0,
    (lambda result_count : result_count >= 0),
    '>= 0',
)


# threads

def parse_threads(data):
    """
    Parses the used threads out from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    threads : ``None | tuple<Channel>``
    """
    channel_datas = data.get('threads', None)
    if (channel_datas is None) or (not channel_datas):
        threads = None
    else:
        threads = tuple(sorted(Channel.from_data(channel_data) for channel_data in channel_datas))
        
        thread_user_datas = data.get('members', None)
        if (thread_user_datas is not None) and thread_user_datas:
            for thread_user_data in thread_user_datas:
                channel_id = int(thread_user_data['id'])
                
                for thread_channel in threads:
                    if thread_channel.id == channel_id:
                        break
                else:
                    continue
                
                user_id = int(thread_user_data['user_id'])
                user = create_partial_user_from_id(user_id)
                thread_user_create(thread_channel, user, thread_user_data)
    
    return threads


def put_threads(threads, data, defaults, *, messages = None):
    """
    Serialises the given threads into the given data.
    
    Parameters
    ----------
    threads : ``None | tuple<Channel>``
        The value to serialise.
    
    data : `dict<str, object>`
        Data to serialise into.
    
    defaults : `bool`
        Whether fields as their default should be included as well.
    
    messages : ``None | tuple<Message>`` = `None`, Optional (Keyword only)
        Messages to detect author guild profiles from.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if (threads is not None) or defaults:
        if threads is None:
            channel_datas = []
            thread_user_datas = []
        
        else:
            channel_datas = [channel.to_data(defaults = defaults, include_internals = True) for channel in threads]
            thread_user_datas = []
            
            if (messages is not None):
                for message in messages:
                    channel_id = message.channel_id
                    for thread_channel in threads:
                        if thread_channel.id == channel_id:
                            break
                    else:
                        continue
                    
                    user = message.author
                    thread_profiles = user.thread_profiles
                    if thread_profiles is None:
                        continue
                    
                    try:
                        thread_profile = thread_profiles[channel_id]
                    except KeyError:
                        continue
                    
                    thread_profile_data = thread_profile.to_data(defaults = defaults, include_internals = True)
                    thread_profile_data['id'] = str(channel_id)
                    thread_profile_data['user_id'] = str(user.id)
                    thread_user_datas.append(thread_profile_data)
            
        data['threads'] = channel_datas
        data['members'] = thread_user_datas
    
    return data


validate_threads = nullable_entity_array_validator_factory('channels', Channel)

from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....channel import Channel, ChannelType
from ....message import Message
from ....user import ThreadProfile, User

from ..fields import put_threads


def _iter_options():
    channel_id_0 = 202601080000
    channel_name_0 = 'Far'
    
    channel_id_1 = 202601080001
    channel_name_1 = 'East'
    
    user_id_0 = 202601080002
    user_id_1 = 202601080003
    
    message_id_0 = 202601080004
    message_id_1 = 202601080005
    
    channel_0 = Channel.precreate(
        channel_id_0,
        channel_type = ChannelType.guild_thread_public,
        name = channel_name_0,
    )
    
    channel_1 = Channel.precreate(
        channel_id_1,
        channel_type = ChannelType.guild_thread_public,
        name = channel_name_1,
    )
    
    thread_profile_0 = ThreadProfile(
        joined_at = DateTime(2015, 6, 7, tzinfo = TimeZone.utc),
    )
    
    thread_profile_1 = ThreadProfile(
        joined_at = DateTime(2015, 6, 8, tzinfo = TimeZone.utc),
    )
    
    user_0 = User.precreate(
        user_id_0,
    )
    user_0.thread_profiles = {
        channel_id_1 : thread_profile_0,
    }
    
    user_1 = User.precreate(
        user_id_1,
    )
    user_1.thread_profiles = {
        channel_id_0 : thread_profile_1,
    }
    
    message_0 = Message.precreate(
        message_id_0,
        author = user_0,
        channel_id = channel_id_1,
    )
    
    message_1 = Message.precreate(
        message_id_1,
        author = user_1,
        channel_id = channel_id_0,
    )
    
    yield (
        None,
        False,
        None,
        {},
    )
    
    yield (
        None,
        True,
        None,
        {
            'threads': [],
            'members': [],
        },
    )
    
    yield (
        (
            channel_0,
            channel_1,
        ),
        False,
        (
            message_0,
            message_1,
        ),
        
        {
            'threads': [
                channel_0.to_data(defaults = False, include_internals = True),
                channel_1.to_data(defaults = False, include_internals = True),
            ],
            'members': [
                {
                    **thread_profile_0.to_data(defaults = False, include_internals = True),
                    'user_id': str(user_id_0),
                    'id': str(channel_id_1),
                },
                {
                    **thread_profile_1.to_data(defaults = False, include_internals = True),
                    'user_id': str(user_id_1),
                    'id': str(channel_id_0),
                },
            ],
        },
    )
    
    yield (
        (
            channel_0,
            channel_1,
        ),
        True,
        (
            message_0,
            message_1,
        ),
        
        {
            'threads': [
                channel_0.to_data(defaults = True, include_internals = True),
                channel_1.to_data(defaults = True, include_internals = True),
            ],
            'members': [
                {
                    **thread_profile_0.to_data(defaults = True, include_internals = True),
                    'user_id': str(user_id_0),
                    'id': str(channel_id_1),
                },
                {
                    **thread_profile_1.to_data(defaults = True, include_internals = True),
                    'user_id': str(user_id_1),
                    'id': str(channel_id_0),
                },
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_threads(input_value, defaults, messages):
    """
    Tests whether ``put_threads`` works as intended.
    
    Parameters
    ----------
    input_value : ``None | tuple<Channel>``
        The value to serialise.
    
    defaults : `bool`
        Whether fields as their default should be included as well.
    
    messages : ``None | tuple<Message>`` = `None`, Optional (Keyword only)
        Messages to detect author guild profiles from.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_threads(input_value, {}, defaults, messages = messages)

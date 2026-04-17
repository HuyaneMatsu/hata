from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....channel import Channel, ChannelType
from ....user import ThreadProfile, User

from ..fields import parse_threads


def _iter_options():
    channel_id_0 = 202601070011
    channel_name_0 = 'Far'
    
    channel_id_1 = 202601070012
    channel_name_1 = 'East'
    
    user_id_0 = 202601070013
    user_id_1 = 202601070014
    
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
    
    user_0 = User.precreate(
        user_id_0,
    )
    
    user_1 = User.precreate(
        user_id_1,
    )
    
    thread_profile_0 = ThreadProfile(
        joined_at = DateTime(2015, 6, 7, tzinfo = TimeZone.utc),
    )
    
    thread_profile_1 = ThreadProfile(
        joined_at = DateTime(2015, 6, 8, tzinfo = TimeZone.utc),
    )
    
    yield (
        {},
        [],
        (
            None,
            {},
        ),
    )
    
    yield (
        {
            'threads': [
                channel_0.to_data(include_internals = True),
                channel_1.to_data(include_internals = True),
            ],
            'members': [
                {
                    **thread_profile_0.to_data(include_internals = True),
                    'user_id': str(user_id_0),
                    'id': str(channel_id_1),
                },
                {
                    **thread_profile_1.to_data(include_internals = True),
                    'user_id': str(user_id_1),
                    'id': str(channel_id_0),
                },
            ],
        },
        [
            user_0,
            user_1,
        ],
        (
            (
                channel_0,
                channel_1,
            ),
            {
                (user_id_0, channel_id_1) : thread_profile_0,
                (user_id_1, channel_id_0) : thread_profile_1,
            },
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_threads(input_data, user_cache):
    """
    Tests whether ``parse_threads`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    user_cache : ``list<ClientUserBase>``
        Users to keep cached for thread profile creation.
    
    Returns
    -------
    output_and_user_thread_profiles : ``(None | tuple<Channel>, dict<(int, int), ThreadProfile>)``
    """
    output = parse_threads(input_data)
    
    user_thread_profiles = {}
    
    if (output is not None):
        for user in user_cache:
            thread_profiles = user.thread_profiles
            if thread_profiles is None:
                continue
            
            for channel in output:
                try:
                    thread_profile = thread_profiles[channel.id]
                except KeyError:
                    continue
                
                break
            
            else:
                continue
            
            user_thread_profiles[user.id, channel.id] = thread_profile
            continue
    
    return output, user_thread_profiles

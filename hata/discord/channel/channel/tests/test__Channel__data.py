from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....client import Client
from ....core import CHANNELS
from ....guild import Guild
from ....user import User
from ....utils import datetime_to_unix_time

from ..channel import Channel
from ..preinstanced import ChannelType
from ..utils import create_partial_channel_from_id


def test__Channel__from_data__default():
    """
    Tests whether ``Channel.from_data`` works as intended.
    
    Case: default.
    """
    channel_id = 202209180139
    guild_id = 202209180140
    name = 'BURNING'
    channel_type = ChannelType.guild_text
    
    data = {
        'id': str(channel_id),
        'name': name,
        'type': channel_type.value,
    }
    
    channel = Channel.from_data(data, None, guild_id)
    
    vampytest.assert_instance(channel, Channel)
    
    vampytest.assert_in(channel_id, CHANNELS)
    vampytest.assert_is(CHANNELS[channel_id], channel)
    
    vampytest.assert_is(channel.type, channel_type)
    vampytest.assert_eq(channel.id, channel_id)
    vampytest.assert_eq(channel.guild_id, guild_id)
    vampytest.assert_eq(channel.name, name)


def test__Channel__from_data__exists():
    """
    Tests whether ``Channel.from_data`` works as intended.
    
    Case: channel already exists.
    """
    channel_id = 202209180141
    guild_id = 202209180142
    name = 'BURNING'
    channel_type = ChannelType.guild_text
    
    existing_channel = create_partial_channel_from_id(channel_id, channel_type, guild_id)
    
    data = {
        'id': str(channel_id),
        'name': name,
        'type': channel_type.value,
    }
    
    channel = Channel.from_data(data, None, guild_id)
    
    vampytest.assert_instance(channel, Channel)
    vampytest.assert_is(channel, existing_channel)


def test__Channel__from_data__guild_channel():
    """
    Tests whether ``Channel.from_data`` works as intended.
    
    Case: guild channel.
    """
    channel_id = 202306130006
    guild_id = 202306130007
    name = 'BURNING'
    channel_type = ChannelType.guild_text
    
    data = {
        'id': str(channel_id),
        'name': name,
        'type': channel_type.value,
    }
    
    guild = Guild.precreate(guild_id)
    
    channel = Channel.from_data(data, None, guild_id)
    
    vampytest.assert_eq(guild.channels, {channel_id: channel})


def test__Channel__from_data__guild_channel_no_string_cache():
    """
    Tests whether ``Channel.from_data`` works as intended.
    
    Case: guild channel, `strong_cache` given as `False`.
    """
    channel_id = 202306130008
    guild_id = 202306130009
    name = 'BURNING'
    channel_type = ChannelType.guild_text
    
    data = {
        'id': str(channel_id),
        'name': name,
        'type': channel_type.value,
    }
    
    guild = Guild.precreate(guild_id)
    
    channel = Channel.from_data(data, None, guild_id, strong_cache = False)
    
    vampytest.assert_eq(guild.channels, {})


def test__Channel__from_data__guild_thread():
    """
    Tests whether ``Channel.from_data`` works as intended.
    
    Case: guild thread.
    """
    channel_id = 202306130010
    guild_id = 202306130011
    name = 'BURNING'
    channel_type = ChannelType.guild_thread_public
    
    data = {
        'id': str(channel_id),
        'name': name,
        'type': channel_type.value,
    }
    
    guild = Guild.precreate(guild_id)
    
    channel = Channel.from_data(data, None, guild_id)
    
    vampytest.assert_eq(guild.threads, {channel_id: channel})


def test__Channel__from_data__guild_thread_no_strong_cache():
    """
    Tests whether ``Channel.from_data`` works as intended.
    
    Case: guild thread, `strong_cache` given as `False`.
    """
    channel_id = 202306130012
    guild_id = 202306130013
    name = 'BURNING'
    channel_type = ChannelType.guild_thread_public
    
    data = {
        'id': str(channel_id),
        'name': name,
        'type': channel_type.value,
    }
    
    guild = Guild.precreate(guild_id)
    
    channel = Channel.from_data(data, None, guild_id, strong_cache = False)
    
    vampytest.assert_eq(guild.threads, None)


def test__Channel__from_data__private():
    """
    Tests whether ``Channel.from_data`` works as intended.
    
    Case: private.
    """
    channel_id = 202306130014
    client_id = 202306130015
    user_id = 202306130016
    
    name = 'BURNING'
    channel_type = ChannelType.private
    
    user = User.precreate(user_id)
    
    client = Client(
        token = 'token_20230613_0000',
        client_id = client_id
    )
    
    try:
        data = {
            'id': str(channel_id),
            'name': name,
            'type': channel_type.value,
            'recipients': [user.to_data(include_internals = True)],
        }
        
        channel = Channel.from_data(data, client, 0)
        
        vampytest.assert_eq(client.private_channels, {user_id: channel})
    
    # Cleanup
    finally:
        client._delete()
        client = None


def test__Channel__from_data__private_no_string_cache():
    """
    Tests whether ``Channel.from_data`` works as intended.
    
    Case: private, `strong_cache` given as `False`.
    """
    channel_id = 202306130017
    client_id = 202306130018
    user_id = 202306130019
    
    name = 'BURNING'
    channel_type = ChannelType.private
    
    user = User.precreate(user_id)
    
    client = Client(
        token = 'token_20230613_0001',
        client_id = client_id
    )
    
    try:
        data = {
            'id': str(channel_id),
            'name': name,
            'type': channel_type.value,
            'recipients': [user.to_data(include_internals = True)],
        }
        
        channel = Channel.from_data(data, client, 0, strong_cache = False)
        
        vampytest.assert_eq(client.private_channels, {})

    # Cleanup
    finally:
        client._delete()
        client = None


def test__Channel__from_data__private_group():
    """
    Tests whether ``Channel.from_data`` works as intended.
    
    Case: private group.
    """
    channel_id = 202306130020
    client_id = 202306130021
    
    name = 'BURNING'
    channel_type = ChannelType.private_group
    
    client = Client(
        token = 'token_20230613_0002',
        client_id = client_id
    )
    
    try:
        data = {
            'id': str(channel_id),
            'name': name,
            'type': channel_type.value,
        }
        
        channel = Channel.from_data(data, client, 0)
        
        vampytest.assert_eq(client.group_channels, {channel_id: channel})
    
    # Cleanup
    finally:
        client._delete()
        client = None


def test__Channel__from_data__private_group_no_strong_cache():
    """
    Tests whether ``Channel.from_data`` works as intended.
    
    Case: private group, `strong_cache` given as `False`.
    """
    channel_id = 202306130022
    client_id = 202306130023
    
    name = 'BURNING'
    channel_type = ChannelType.private_group
    
    client = Client(
        token = 'token_20230613_0003',
        client_id = client_id
    )
    
    try:
        data = {
            'id': str(channel_id),
            'name': name,
            'type': channel_type.value,
        }
        
        channel = Channel.from_data(data, client, 0, strong_cache = False)
        
        vampytest.assert_eq(client.group_channels, {})

    # Cleanup
    finally:
        client._delete()
        client = None


def test__Channel__to_data__default():
    """
    Tests whether ``Channel.to_data`` works as intended.
    
    Case: include internals & defaults.
    """
    channel_id = 202209180143
    guild_id = 202209180144
    name = 'BURNING'
    channel_type = ChannelType.guild_text
    
    channel = Channel.precreate(channel_id, channel_type = channel_type, name = name, guild_id = guild_id)
    
    data = channel.to_data(defaults = True, include_internals = True)
    
    vampytest.assert_in('id', data)
    vampytest.assert_in('guild_id', data)
    vampytest.assert_in('name', data)
    vampytest.assert_in('type', data)
    
    vampytest.assert_eq(data['id'], str(channel_id))
    vampytest.assert_eq(data['guild_id'], str(guild_id))
    vampytest.assert_eq(data['name'], name)
    vampytest.assert_eq(data['type'], channel_type.value)


def test__Channel__update_attributes():
    """
    Tests whether ``Channel._update_attributes`` works as intended.
    """
    channel_id = 202509230000
    guild_id = 202509230001
    channel_type = ChannelType.guild_voice
    
    old_name = 'BURNING'
    
    new_name = 'RED'
    
    channel = Channel.precreate(channel_id, channel_type = channel_type, name = old_name, guild_id = guild_id)
    
    channel._update_attributes({
        'name': new_name,
        'type': channel_type.value,
    })
    
    vampytest.assert_eq(channel.name, new_name)


def test__Channel__difference_update_attributes():
    """
    Tests whether ``Channel._difference_update_attributes`` works as intended.
    """
    channel_id = 202509230002
    guild_id = 202509230003
    channel_type = ChannelType.guild_text
    
    old_name = 'BURNING'
    
    new_name = 'RED'
    
    channel = Channel.precreate(channel_id, channel_type = channel_type, name = old_name, guild_id = guild_id)
    
    old_attributes = channel._difference_update_attributes({
        'name': new_name,
        'type': channel_type.value,
    })
    
    vampytest.assert_eq(channel.name, new_name)
    
    vampytest.assert_eq(
        old_attributes,
        {
            'name': old_name,
        },
    )


def test__Channel__from_partial_data():
    """
    Tests whether ``Channel._from_partial_data`` works as intended.
    """
    channel_id = 202209180136
    guild_id = 202209180137
    name = 'BURNING'
    channel_type = ChannelType.guild_text
    
    data = {
        'id': str(channel_id),
        'name': name,
        'type': channel_type.value,
    }
    
    channel = Channel._from_partial_data(data, channel_id, guild_id)
    
    vampytest.assert_instance(channel, Channel)
    
    vampytest.assert_is(channel.type, channel_type)
    vampytest.assert_eq(channel.id, channel_id)
    vampytest.assert_eq(channel.guild_id, guild_id)
    vampytest.assert_eq(channel.name, name)
    
    # This method should not cache
    vampytest.assert_not_in(channel_id, CHANNELS)


def test__Channel__update_status():
    """
    Tests whether ``Channel._update_status`` works as intended.
    """
    channel_id = 202209180143
    guild_id = 202209180144
    channel_type = ChannelType.guild_voice
    
    old_status = 'blaze'
    
    new_status = 'rollin'
    
    channel = Channel.precreate(channel_id, channel_type = channel_type, status = old_status, guild_id = guild_id)
    
    channel._update_status({
        'status': new_status,
        'type': channel_type.value,
    })
    
    vampytest.assert_eq(channel.status, new_status)


def test__Channel__difference_update_status():
    """
    Tests whether ``Channel._difference_update_status`` works as intended.
    """
    channel_id = 202209180143
    guild_id = 202209180144
    channel_type = ChannelType.guild_voice
    
    old_status = 'blaze'
    
    new_status = 'rollin'
    
    channel = Channel.precreate(channel_id, channel_type = channel_type, status = old_status, guild_id = guild_id)
    
    old_attributes = channel._difference_update_status({
        'status': new_status,
        'type': channel_type.value,
    })
    
    vampytest.assert_eq(channel.status, new_status)
    
    vampytest.assert_eq(
        old_attributes,
        {
            'status': old_status,
        },
    )


def test__Channel__update_voice_engaged_since():
    """
    Tests whether ``Channel._update_voice_engaged_since`` works as intended.
    """
    channel_id = 202209180143
    guild_id = 202209180144
    channel_type = ChannelType.guild_voice
    
    old_voice_engaged_since = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    new_voice_engaged_since = DateTime(2016, 5, 17, tzinfo = TimeZone.utc)
    
    channel = Channel.precreate(
        channel_id, channel_type = channel_type, voice_engaged_since = old_voice_engaged_since, guild_id = guild_id
    )
    
    channel._update_voice_engaged_since({
        'voice_start_time': datetime_to_unix_time(new_voice_engaged_since),
        'type': channel_type.value,
    })
    
    vampytest.assert_eq(channel.voice_engaged_since, new_voice_engaged_since)


def test__Channel__difference_update_voice_engaged_since():
    """
    Tests whether ``Channel._difference_update_voice_engaged_since`` works as intended.
    """
    channel_id = 202209180143
    guild_id = 202209180144
    channel_type = ChannelType.guild_voice
    
    old_voice_engaged_since = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    new_voice_engaged_since = DateTime(2016, 5, 17, tzinfo = TimeZone.utc)
    
    channel = Channel.precreate(
        channel_id, channel_type = channel_type, voice_engaged_since = old_voice_engaged_since, guild_id = guild_id
    )
    
    old_attributes = channel._difference_update_voice_engaged_since({
        'voice_start_time': datetime_to_unix_time(new_voice_engaged_since),
        'type': channel_type.value,
    })
    
    vampytest.assert_eq(channel.voice_engaged_since, new_voice_engaged_since)
    
    vampytest.assert_eq(
        old_attributes,
        {
            'voice_engaged_since': old_voice_engaged_since,
        },
    )

import vampytest

from ..key import EmbeddedActivityStateKey

from .test__EmbeddedActivityStateKey__constructor import _assert_are_fields_set


def test__EmbeddedActivityStateKey__from_data__0():
    """
    Tests whether ``EmbeddedActivityStateKey.from_data`` works as intended.
    
    Case: No guild_oid given.
    """
    application_id = 202212260005
    channel_id = 202212260006
    guild_id = 202212260007
    
    data = {
        'embedded_activity': {'application_id': str(application_id)},
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
    }
    
    key = EmbeddedActivityStateKey.from_data(data, 0)
    _assert_are_fields_set(key)
    
    vampytest.assert_eq(key.application_id, application_id)
    vampytest.assert_eq(key.channel_id, channel_id)
    vampytest.assert_eq(key.guild_id, guild_id)


def test__EmbeddedActivityStateKey__from_data__1():
    """
    Tests whether ``EmbeddedActivityStateKey.from_data`` works as intended.
    
    Case: guild_id given.
    """
    application_id = 202212260008
    channel_id = 202212260009
    guild_id = 202212260010
    
    data = {
        'embedded_activity': {'application_id': str(application_id)},
        'channel_id': str(channel_id),
    }
    
    key = EmbeddedActivityStateKey.from_data(data, guild_id)
    _assert_are_fields_set(key)
    
    vampytest.assert_eq(key.application_id, application_id)
    vampytest.assert_eq(key.channel_id, channel_id)
    vampytest.assert_eq(key.guild_id, guild_id)


def test__EmbeddedActivityStateKey__to_data():
    """
    Tests whether ``EmbeddedActivityStateKey.to_data`` works as intended.
    
    Case: Include defaults.
    """
    application_id = 202212260011
    channel_id = 202212260012
    guild_id = 202212260013
    
    expected_data = {
        'embedded_activity': {'application_id': str(application_id)},
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
    }
    
    key = EmbeddedActivityStateKey(guild_id, channel_id, application_id)
    
    vampytest.assert_eq(
        key.to_data(defaults = True),
        expected_data,
    )

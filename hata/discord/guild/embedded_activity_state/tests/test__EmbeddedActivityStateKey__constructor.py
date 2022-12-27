import vampytest

from ..key import EmbeddedActivityStateKey


def _assert_are_fields_set(key):
    """
    Asserts whether every attributes is set of the given key.
    
    Parameters
    ----------
    key : ``EmbeddedActivityStateKey``
        The key to check.
    """
    vampytest.assert_instance(key, EmbeddedActivityStateKey)
    vampytest.assert_instance(key.application_id, int)
    vampytest.assert_instance(key.channel_id, int)
    vampytest.assert_instance(key.guild_id, int)


def test__EmbeddedActivityStateKey__new():
    """
    Tests whether ``EmbeddedActivityStateKey.__new__`` works as intended.
    """
    application_id = 202212260002
    channel_id = 202212260003
    guild_id = 202212260004
    
    key = EmbeddedActivityStateKey(guild_id, channel_id, application_id)
    _assert_are_fields_set(key)
    
    vampytest.assert_eq(key.application_id, application_id)
    vampytest.assert_eq(key.channel_id, channel_id)
    vampytest.assert_eq(key.guild_id, guild_id)

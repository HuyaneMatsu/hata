import vampytest

from ..key import EmbeddedActivityStateKey

from .test__EmbeddedActivityStateKey__constructor import _assert_are_fields_set


def test__EmbeddedActivityStateKey__copy():
    """
    Tests whether ``EmbeddedActivityStateKey.copy`` works as intended.
    """
    application_id = 202212260029
    channel_id = 202212260030
    guild_id = 202212260031
    
    key = EmbeddedActivityStateKey(guild_id, channel_id, application_id)
    
    copy = key.copy()
    _assert_are_fields_set(copy)
    vampytest.assert_is_not(key, copy)
    
    vampytest.assert_eq(key, copy)


def test__EmbeddedActivityStateKey__copy_with__0():
    """
    Tests whether ``EmbeddedActivityStateKey.copy_with`` works as intended.
    
    Case: No fields given.
    """
    application_id = 202212260032
    channel_id = 202212260033
    guild_id = 202212260034
    
    key = EmbeddedActivityStateKey(guild_id, channel_id, application_id)
    
    copy = key.copy_with()
    _assert_are_fields_set(copy)
    vampytest.assert_is_not(key, copy)
    
    vampytest.assert_eq(key, copy)

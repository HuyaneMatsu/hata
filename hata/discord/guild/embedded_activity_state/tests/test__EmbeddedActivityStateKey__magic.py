import vampytest

from ..key import EmbeddedActivityStateKey


def test__EmbeddedActivityStateKey__repr():
    """
    Tests whether ``EmbeddedActivityStateKey.__repr__`` works as intended.
    """
    application_id = 202212260014
    channel_id = 202212260015
    guild_id = 202212260016
    
    key = EmbeddedActivityStateKey(guild_id, channel_id, application_id)
    vampytest.assert_instance(repr(key), str)


def test__EmbeddedActivityStateKey__hash():
    """
    Tests whether ``EmbeddedActivityStateKey.__hash__`` works as intended.
    """
    application_id = 202212260017
    channel_id = 202212260018
    guild_id = 202212260019
    
    key = EmbeddedActivityStateKey(guild_id, channel_id, application_id)
    vampytest.assert_instance(hash(key), int)


def test__EmbeddedActivityStateKey__eq():
    """
    Tests whether ``EmbeddedActivityStateKey.__hash__`` works as intended.
    """
    application_id = 202212260020
    channel_id = 202212260021
    guild_id = 202212260022
    
    keyword_parameters = {
        'application_id': application_id,
        'channel_id': channel_id,
        'guild_id': guild_id
    }
    
    key = EmbeddedActivityStateKey(**keyword_parameters)
    vampytest.assert_eq(key, key)
    vampytest.assert_ne(key, object())
    
    for field_name, field_value in (
        ('application_id', 202212260023),
        ('channel_id', 202212260024),
        ('guild_id', 202212260025),
    ):
        test_key = EmbeddedActivityStateKey(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(key, test_key)


def test__EmbeddedActivityStateKey__unpack():
    """
    Tests whether ``EmbeddedActivityStateKey.__hash__`` works as intended.
    """
    application_id = 202212260026
    channel_id = 202212260027
    guild_id = 202212260028
    
    key = EmbeddedActivityStateKey(guild_id, channel_id, application_id)
    
    length = len(key)
    vampytest.assert_instance(length, int)
    
    unpacked = [*key]
    vampytest.assert_eq(len(unpacked), length)
    
    vampytest.assert_in(application_id, unpacked)
    vampytest.assert_in(channel_id, unpacked)
    vampytest.assert_in(guild_id, unpacked)

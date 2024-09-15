import vampytest

from ..embedded_activity_location import EmbeddedActivityLocation
from ..preinstanced import EmbeddedActivityLocationType

from .test__EmbeddedActivityLocation__constructor import _assert_are_fields_set


def test__EmbeddedActivityLocation__copy():
    """
    Tests whether ``EmbeddedActivityLocation.copy`` works as intended.
    """
    channel_id = 202409010047
    guild_id = 202409010048
    location_type = EmbeddedActivityLocationType.guild_channel
    
    embedded_activity_location = EmbeddedActivityLocation(
        guild_id = guild_id,
        channel_id = channel_id,
        location_type = location_type,
    )
    
    copy = embedded_activity_location.copy()
    _assert_are_fields_set(copy)
    vampytest.assert_is_not(embedded_activity_location, copy)
    
    vampytest.assert_eq(embedded_activity_location, copy)


def test__EmbeddedActivityLocation__copy_with__no_fields():
    """
    Tests whether ``EmbeddedActivityLocation.copy_with`` works as intended.
    
    Case: No fields given.
    """
    channel_id = 202409010049
    guild_id = 202409010050
    location_type = EmbeddedActivityLocationType.guild_channel
    
    embedded_activity_location = EmbeddedActivityLocation(
        guild_id = guild_id,
        channel_id = channel_id,
        location_type = location_type,
    )
    
    copy = embedded_activity_location.copy_with()
    _assert_are_fields_set(copy)
    vampytest.assert_is_not(embedded_activity_location, copy)
    
    vampytest.assert_eq(embedded_activity_location, copy)


def test__EmbeddedActivityLocation__copy_with__all_fields():
    """
    Tests whether ``EmbeddedActivityLocation.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_channel_id = 202409010051
    old_guild_id = 202409010052
    old_location_type = EmbeddedActivityLocationType.guild_channel
    
    new_channel_id = 202409010053
    new_guild_id = 202409010054
    new_location_type = EmbeddedActivityLocationType.private_channel
    
    embedded_activity_location = EmbeddedActivityLocation(
        guild_id = old_guild_id,
        channel_id = old_channel_id,
        location_type = old_location_type,
    )
    
    copy = embedded_activity_location.copy_with(
        guild_id = new_guild_id,
        channel_id = new_channel_id,
        location_type = new_location_type,
    )
    _assert_are_fields_set(copy)
    vampytest.assert_is_not(embedded_activity_location, copy)
    
    vampytest.assert_ne(embedded_activity_location, copy)
    
    vampytest.assert_eq(copy.channel_id, new_channel_id)
    vampytest.assert_eq(copy.guild_id, new_guild_id)
    vampytest.assert_is(copy.type, new_location_type)

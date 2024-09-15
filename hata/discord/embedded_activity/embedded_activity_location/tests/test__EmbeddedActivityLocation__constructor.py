import vampytest

from ..embedded_activity_location import EmbeddedActivityLocation
from ..preinstanced import EmbeddedActivityLocationType


def _assert_are_fields_set(embedded_activity_location):
    """
    Asserts whether every attributes is set of the given embedded activity location.
    
    Parameters
    ----------
    embedded_activity_location : ``EmbeddedActivityLocation``
        The embedded activity location to check.
    """
    vampytest.assert_instance(embedded_activity_location, EmbeddedActivityLocation)
    vampytest.assert_instance(embedded_activity_location.type, EmbeddedActivityLocationType)
    vampytest.assert_instance(embedded_activity_location.channel_id, int)
    vampytest.assert_instance(embedded_activity_location.guild_id, int)


def test__EmbeddedActivityLocation__new__no_fields():
    """
    Tests whether ``EmbeddedActivityLocation.__new__`` works as intended.
    
    Case: No fields given.
    """
    embedded_activity_location = EmbeddedActivityLocation()
    _assert_are_fields_set(embedded_activity_location)


def test__EmbeddedActivityLocation__new__all_fields():
    """
    Tests whether ``EmbeddedActivityLocation.__new__`` works as intended.
    
    Case: All fields given.
    """
    channel_id = 202409010033
    guild_id = 202409010034
    location_type = EmbeddedActivityLocationType.guild_channel
    
    embedded_activity_location = EmbeddedActivityLocation(
        guild_id = guild_id,
        channel_id = channel_id,
        location_type = location_type,
    )
    _assert_are_fields_set(embedded_activity_location)
    
    vampytest.assert_eq(embedded_activity_location.channel_id, channel_id)
    vampytest.assert_eq(embedded_activity_location.guild_id, guild_id)
    vampytest.assert_is(embedded_activity_location.type, location_type)

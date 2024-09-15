import vampytest

from ..embedded_activity_location import EmbeddedActivityLocation
from ..preinstanced import EmbeddedActivityLocationType

from .test__EmbeddedActivityLocation__constructor import _assert_are_fields_set


def test__EmbeddedActivityLocation__from_data__0():
    """
    Tests whether ``EmbeddedActivityLocation.from_data`` works as intended.
    
    Case: No guild_oid given.
    """
    channel_id = 202409010035
    guild_id = 202409010036
    location_type = EmbeddedActivityLocationType.guild_channel
    
    data = {
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
        'kind': location_type.value,
    }
    
    embedded_activity_location = EmbeddedActivityLocation.from_data(data)
    _assert_are_fields_set(embedded_activity_location)
    
    vampytest.assert_eq(embedded_activity_location.channel_id, channel_id)
    vampytest.assert_eq(embedded_activity_location.guild_id, guild_id)
    vampytest.assert_is(embedded_activity_location.type, location_type)


def test__EmbeddedActivityLocation__to_data():
    """
    Tests whether ``EmbeddedActivityLocation.to_data`` works as intended.
    
    Case: Include defaults.
    """
    channel_id = 202409010037
    guild_id = 202409010038
    location_type = EmbeddedActivityLocationType.guild_channel
    
    embedded_activity_location = EmbeddedActivityLocation(
        guild_id = guild_id,
        channel_id = channel_id,
        location_type = location_type,
    )
    
    vampytest.assert_eq(
        embedded_activity_location.to_data(defaults = True),
        {
            'channel_id': str(channel_id),
            'guild_id': str(guild_id),
            'kind': location_type.value,
        },
    )

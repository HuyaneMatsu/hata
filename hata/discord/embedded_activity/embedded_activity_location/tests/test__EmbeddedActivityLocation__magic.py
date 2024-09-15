import vampytest

from ..embedded_activity_location import EmbeddedActivityLocation
from ..preinstanced import EmbeddedActivityLocationType


def test__EmbeddedActivityLocation__repr():
    """
    Tests whether ``EmbeddedActivityLocation.__repr__`` works as intended.
    """
    channel_id = 202409010039
    guild_id = 202409010040
    location_type = EmbeddedActivityLocationType.guild_channel
    
    embedded_activity_location = EmbeddedActivityLocation(
        guild_id = guild_id,
        channel_id = channel_id,
        location_type = location_type,
    )
    vampytest.assert_instance(repr(embedded_activity_location), str)


def test__EmbeddedActivityLocation__hash():
    """
    Tests whether ``EmbeddedActivityLocation.__hash__`` works as intended.
    """
    channel_id = 202409010041
    guild_id = 202409010042
    location_type = EmbeddedActivityLocationType.guild_channel
    
    embedded_activity_location = EmbeddedActivityLocation(
        guild_id = guild_id,
        channel_id = channel_id,
        location_type = location_type,
    )
    vampytest.assert_instance(hash(embedded_activity_location), int)


def _iter_options__eq():
    channel_id = 202409010043
    guild_id = 202409010044
    location_type = EmbeddedActivityLocationType.guild_channel
    
    keyword_parameters = {
        'channel_id': channel_id,
        'guild_id': guild_id,
        'location_type': location_type,
    }
    
    yield (
        {},
        {},
        True,
    )
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'channel_id': 202409010045,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'guild_id': 202409010046,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'location_type': EmbeddedActivityLocationType.private_channel,
        },
        False,
    )
    
    

@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__EmbeddedActivityLocation__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``EmbeddedActivityLocation.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    embedded_activity_location_0 = EmbeddedActivityLocation(**keyword_parameters_0)
    embedded_activity_location_1 = EmbeddedActivityLocation(**keyword_parameters_1)
    
    output = embedded_activity_location_0 == embedded_activity_location_1
    vampytest.assert_instance(output, bool)
    return output

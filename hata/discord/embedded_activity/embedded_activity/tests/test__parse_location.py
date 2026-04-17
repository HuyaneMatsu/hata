import vampytest

from ...embedded_activity_location import EmbeddedActivityLocation

from ..fields import parse_location


def _iter_options():
    location = EmbeddedActivityLocation(guild_id = 202409010080)
    
    yield ({}, None)
    yield ({'location': None}, None)
    yield ({'location': location.to_data()}, location)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_location(input_data):
    """
    Tests whether ``parse_location`` works as intended.
    
    Parameters
    ----------
    input_data : dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | EmbeddedActivityLocation`
    """
    output = parse_location(input_data)
    vampytest.assert_instance(output, EmbeddedActivityLocation, nullable = True)
    return output

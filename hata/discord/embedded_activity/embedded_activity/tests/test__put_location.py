import vampytest

from ...embedded_activity_location import EmbeddedActivityLocation

from ..fields import put_location


def _iter_options():
    location = EmbeddedActivityLocation(guild_id = 202409010082)
    
    yield None, False, {'location': None}
    yield None, True, {'location': None}
    yield location, False, {'location': location.to_data()}
    yield location, True, {'location': location.to_data(defaults = True)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_location(input_value, defaults):
    """
    Tests whether ``put_location`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | EmbeddedActivityLocation`
        Value to serialise.
    defaults : `bool`
        Whether fields with their default value should be included.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_location(input_value, {}, defaults)

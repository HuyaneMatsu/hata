import vampytest

from ...embedded_activity_location import EmbeddedActivityLocation

from ..fields import validate_location


def _iter_options__passing():
    location = EmbeddedActivityLocation(channel_id = 202409040045)
    
    yield None, None
    yield location, location


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_location(input_value):
    """
    Tests whether `validate_location` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | EmbeddedActivityLocation`
    
    Raises
    ------
    TypeError
    """
    output = validate_location(input_value)
    vampytest.assert_instance(output, EmbeddedActivityLocation, nullable = True)
    return output

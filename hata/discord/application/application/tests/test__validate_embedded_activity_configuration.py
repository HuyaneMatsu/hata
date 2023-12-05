import vampytest

from ...embedded_activity_configuration import EmbeddedActivityConfiguration

from ..fields import validate_embedded_activity_configuration


def _iter_options__passing():
    embedded_activity_configuration = EmbeddedActivityConfiguration(position = 69)
    
    yield None, None
    yield embedded_activity_configuration, embedded_activity_configuration


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_embedded_activity_configuration(input_value):
    """
    Tests whether ``validate_embedded_activity_configuration`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | EmbeddedActivityConfiguration`
    
    Raises
    ------
    TypeError
    """
    return validate_embedded_activity_configuration(input_value)

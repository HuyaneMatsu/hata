import vampytest

from ..fields import validate_overlay_method_flags
from ..flags import ApplicationOverlayMethodFlags


def iter_options__passing():
    yield None, ApplicationOverlayMethodFlags(0)
    yield 1, ApplicationOverlayMethodFlags(1)
    yield ApplicationOverlayMethodFlags(1), ApplicationOverlayMethodFlags(1)


def iter_options__type_error():
    yield 'a'
    yield 12.6


@vampytest._(vampytest.call_from(iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(iter_options__type_error()).raising(TypeError))
def test__validate_overlay_method_flags(input_value):
    """
    Tests whether `validate_overlay_method_flags` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The object to validate.
    
    Returns
    -------
    value : ``ApplicationOverlayMethodFlags``
        The validated value.
    
    Raises
    ------
    TypeError
    """
    output = validate_overlay_method_flags(input_value)
    vampytest.assert_instance(output, ApplicationOverlayMethodFlags)
    return output

import vampytest

from ..fields import validate_enabled


def _iter_options__passing():
    yield True, True
    yield False, False
    yield None, True


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_enabled(input_value):
    """
    Tests whether `validate_enabled` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `bool`
    
    Raises
    ------
    TypeError
    """
    output = validate_enabled(input_value)
    vampytest.assert_instance(output, bool)
    return output
